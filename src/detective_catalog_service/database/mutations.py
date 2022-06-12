# import standard modules
import uuid
from typing import Literal

# import project related module
from detective_catalog_service.settings import dgraph_client
from detective_catalog_service.database.execution import execute_mutation, execute_delete, execute_advanced_mutation


def create_new_catalog(name: str, properties: dict) -> dict:

    xid_value = str(uuid.uuid1())
    xid = f'_:source1 <SourceConnection.xid> "{xid_value}" .\n'
    name = f'_:source1 <SourceConnection.name> "{name}" .\n'
    rdf = '\n'.join(f'_:source1 <SourceConnection.{key}> "{value}" .' for key, value in properties.items())
    status = '\n_:source1 <SourceConnection.status> "pending" .\n'
    node = '\n_:source1 <dgraph.type> "SourceConnection" .'

    mutation = xid + name + rdf + status + node

    if execute_mutation(dgraph_client, mutation):
        return {"success": True, "xid": xid_value}
    else:
        return {"success": False, "xid": xid_value}


def update_status_of_catalog(uid: str, status: Literal["available", "pending", "unavailable"]) -> bool:
    n_quad = f'<{uid}> <SourceConnection.status> "{status}" .'
    if execute_mutation(dgraph_client, n_quad):
        return True
    else:
        return False


def delete_catalog_by_uid(uid: str) -> bool:
    n_quad = f'<{uid}> * * .'
    return execute_delete(dgraph_client, n_quad)


def remove_source_with_schema_by_xid(source_xid: str) -> bool:
    variables = {"$source_xid": source_xid}
    query = """
        query table_and_schema($source_xid: string){
            source_and_schema(func: eq(SourceConnection.xid, $source_xid)){
                source as uid
                SourceConnection.connectedTables {
                    table as uid
                    TableObject.tableSchema {
                        column as uid
                    }
                }
            }
        }
    """
    n_quad = """
      uid(source) * * .
      uid(table) * *  .
      uid(column) * *  .
    """

    status = execute_advanced_mutation(
        client=dgraph_client,
        query=query,
        variables=variables,
        n_quad=n_quad,
        execution_type="delete"
    )
    return status


def update_source_with_schema_by_uid(uid: str, properties: dict) -> bool:
    n_quad = '\n'.join(f'<{uid}> <SourceConnection.{k}> "{v}" .' for k, v in properties.items())
    if execute_mutation(dgraph_client, n_quad):
        return True
    else:
        return False
