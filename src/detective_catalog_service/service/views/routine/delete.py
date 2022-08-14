# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.utils import test_dgraph_connection
from detective_catalog_service.database.queries import check_catalog_in_dgraph
from detective_catalog_service.service.models.payload.routine import DeletePayload
from detective_catalog_service.database.queries import get_source_connection_id_by_xid
from detective_catalog_service.database.mutations import remove_source_with_schema_by_xid, update_status_of_catalog


def delete_routine(payload: DeletePayload) -> dict:
    """
    function deletes a catalog based on it's dgraph xid
    :param payload: deletion payload which
    :return: array holding information about the execution status
    """

    # 1. check if catalog exists in trino and in dgraph
    if test_dgraph_connection():
        engine_check = TrinoOperation.check_catalog_by_name_in_trino(payload.source_connection_name.lower())
        database_check = check_catalog_in_dgraph(payload.source_connection_name, payload.source_connection_xid)

        if all([engine_check, database_check]):
            # 2. delete catalog and related tables in dgraph and trino
            try:
                query_engine_result = TrinoOperation.delete_catalog(payload.source_connection_name.lower())

                if query_engine_result:
                    database_result = remove_source_with_schema_by_xid(payload.source_connection_xid)

                    if database_result:
                        return {"description": "success"}

                    else:
                        try:
                            uid = get_source_connection_id_by_xid(payload.source_connection_xid)
                            if uid != "":
                                update_status_of_catalog(uid, status="Error")
                                return {"error": "3015"}
                            else:
                                return {"error": "3018"}

                        except Exception:
                            return {"error": "3016"}
                else:
                    return {"error": "3001"}

            except Exception:
                return {"error": "3014"}
        else:
            return {"error": f"3002 {engine_check}, {database_check}"}
    else:
        return {"error": "3017"}
