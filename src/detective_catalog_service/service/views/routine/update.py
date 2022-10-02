# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.models.payload.routine import UpdatePayload
from detective_catalog_service.database.queries import get_name_and_uid_of_catalog_from_dgraph
from detective_catalog_service.service.models.response.catalog_requests import RoutineResponse
from detective_catalog_service.database.mutations import update_source_with_schema_by_uid, update_status_of_catalog


def update_routine(payload: UpdatePayload) -> RoutineResponse:
    # 1. check if catalog exists in trino and in dgraph
    status = RoutineResponse()
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
                    status.success = True
                    status.description = "source connection and tables are updated"
                else:
                    update_status_of_catalog(uid, status="Error")
                    status.error = "3010"
            else:
                update_status_of_catalog(uid, status="Error")
                status.error = "3011"
        else:
            update_status_of_catalog(uid, status="Error")
            status.error = "3012"
    else:
        update_status_of_catalog(uid, status="Error")
        status.error = "3013"

    return status
