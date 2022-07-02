# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.database.queries import check_catalog_in_dgraph
from detective_catalog_service.service.models.payload.routine import DeletePayload
from detective_catalog_service.database.mutations import remove_source_with_schema_by_xid


def delete_routine(payload: DeletePayload) -> dict:
    """
    function deletes a catalog based on it's dgraph xid
    :param payload: deletion payload which
    :return: array holding information about the execution status
    """

    # 1. check if catalog exists in trino and in dgraph
    available = {
        "query engine": TrinoOperation.check_catalog_by_name_in_trino(payload.source_connection_name.lower()),
        "database": check_catalog_in_dgraph(payload.source_connection_name, payload.source_connection_xid)
    }

    if all(list(available.values())):
        # 2. delete catalog and related tables in dgraph and trino
        delete = {
            "database": remove_source_with_schema_by_xid(payload.source_connection_xid),
            "query engine": TrinoOperation.delete_catalog(payload.source_connection_name.lower())
        }
        if all(list(delete.values())):
            return {"description": "success"}
        else:
            return {"error": "3001"}

    else:
        return {"error": "3001"}
