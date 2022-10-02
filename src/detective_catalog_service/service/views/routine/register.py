# import standard modules
import asyncio

# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.models.connector.main import PropertyModel
from detective_catalog_service.service.views.routine.crawl import initialize_crawl
from detective_catalog_service.database.queries import check_for_source_connection_name, get_source_connection_id_by_xid
from detective_catalog_service.database.mutations import (
    create_new_catalog,
    update_status_of_catalog,
    delete_catalog_by_uid
)


def register_routine(source_connection: PropertyModel, tenant_id: str) -> dict:
    # 1. Create Catalog in dgraph
    catalog_name = source_connection.name.lower()
    catalog_status = create_new_catalog(source_connection.dict())
    uid = get_source_connection_id_by_xid(catalog_status.get("xid", ""))

    if catalog_status.get("success", False) & (uid != ""):

        # 2. Create Catalog in Trino
        if TrinoOperation.register_catalog(catalog_name, source_connection.as_properties()):

            # 3. check if catalog name exists in both envs
            trino_catalogs = TrinoOperation.list_catalog().get("body", list())
            source_available = check_for_source_connection_name(catalog_name)

            if all([(catalog_name in trino_catalogs), source_available]):
                update_status_of_catalog(uid, status="Available")
                asyncio.create_task(initialize_crawl(uid, tenant_id))
                return {"success": "catalog is now available"}

            else:
                update_status_of_catalog(uid, status="Error")
                return {"error": "3006"}
        else:
            update_status_of_catalog(uid, status="Error")
            if delete_catalog_by_uid(uid):
                return {"error": "3007"}
            else:
                return {"error": "3008"}
    else:
        return {"error": "3009"}
