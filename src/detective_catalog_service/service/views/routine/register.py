# import standard modules
import time

# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.models.main import PropertyModel
from detective_catalog_service.database.queries import check_for_source_connection_name, get_source_connection_id_by_xid
from detective_catalog_service.database.mutations import (
    create_new_catalog,
    update_status_of_catalog,
    delete_catalog_by_uid
)


def register_routine(name: str, source_connection: PropertyModel) -> dict:
    # 1. Create Catalog in dgraph
    catalog_name = name.lower()
    catalog_status = create_new_catalog(catalog_name, source_connection.dict())
    uid = get_source_connection_id_by_xid(catalog_status.get("xid", ""))
    if catalog_status.get("success") & (uid != ""):
        # 2. Create Catalog in Trino
        if TrinoOperation.register_catalog(catalog_name, source_connection.as_properties()):
            # 3. check if catalog name exists in both envs
            trino_catalogs = TrinoOperation.list_catalog().get("body")
            if (catalog_name in trino_catalogs) & check_for_source_connection_name(catalog_name):
                update_status_of_catalog(uid, status="available")
                return {"success": ["catalog is now available"]}
            else:
                update_status_of_catalog(uid, status="unavailable")
                return {"error": ["0001: catalog could not be identified, contact support"]}
        else:
            if delete_catalog_by_uid(uid):
                return {"error": ["0001: catalog could not be registered in query engine, contact support"]}
            else:
                return {"error": [
                    "0001: catalog could not be registered in query engine nor be deleted from db, contact support"]}
    else:
        return {"error": ["0001: catalog could not be registered in database, contact support"]}

