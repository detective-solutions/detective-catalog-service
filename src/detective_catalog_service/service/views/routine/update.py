# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.models.payload.routine import UpdatePayload
from detective_catalog_service.database.queries import get_name_and_uid_of_catalog_from_dgraph
from detective_catalog_service.database.mutations import update_source_with_schema_by_uid, update_status_of_catalog


def update_routine(payload: UpdatePayload) -> dict:
    # 1. check if catalog exists in trino and in dgraph
    uid, catalog_name = get_name_and_uid_of_catalog_from_dgraph(payload.source_connection_xid)
    update_status_of_catalog(uid, status="Pending")
    if (catalog_name != "") & (uid != ""):
        available = {
            "query engine": TrinoOperation.check_catalog_by_name_in_trino(catalog_name.lower()),
            "database": True,
        }
        if all(list(available.values())):
            # 2. update catalog and in dgraph and trino
            if TrinoOperation.update_catalog(catalog_name, payload.source_connection_properties.as_properties()):
                if update_source_with_schema_by_uid(uid, payload.source_connection_properties.dict()):
                    return {"success": "source connection and tables are updated"}
                else:
                    update_status_of_catalog(uid, status="Error")
                    return {"error": "3010"}
            else:
                update_status_of_catalog(uid, status="Error")
                return {"error": "3011"}
        else:
            update_status_of_catalog(uid, status="Error")
            return {"error": "3012"}
    else:
        update_status_of_catalog(uid, status="Error")
        return {"error": "3013"}
