# import standard modules
from typing import List, Dict

# import project related module
from detective_catalog_service.settings import dgraph_client
from detective_catalog_service.database.execution import execute_query


def check_for_source_connection_name(source_name: str) -> bool:
    query = '''
        query connectionNames($source_name: string) { result(func: eq(dgraph.type, "SourceConnection"))
        @filter(eq(SourceConnection.name, $source_name)) {
            name: SourceConnection.name
        }
    }
    '''
    variables = {"$source_name": source_name}
    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        source_names = [x.get("name", "") for x in res.get("result", [])]
        if source_name in source_names:
            return True
        else:
            return False
    else:
        return False


def get_source_connection_id_by_xid(source_connection_xid: str) -> str:
    query = '''
        query connectionNames($xid: string) {result(func: eq(dgraph.type, "SourceConnection"))
        @filter(eq(SourceConnection.xid, $xid)) {
            uid
        }
    }
    '''
    variables = {"$xid": source_connection_xid}
    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        try:
            return str(res["result"][0]["uid"])
        except KeyError:
            return ""
    else:
        return ""


def get_source_connection_id_and_type_by_xid(source_connection_xid: str) -> dict:
    query = '''
        query connectionNames($xid: string) {result(func: eq(dgraph.type, "SourceConnection"))
        @filter(eq(SourceConnection.xid, $xid)) {
            uid
            connectorName: SourceConnection.connectorName
        }
    }
    '''
    variables = {"$xid": source_connection_xid}
    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        try:
            result: dict = res["result"][0]
            return result
        except KeyError:
            return dict()
    else:
        return dict()


def get_source_connection_values(source_uid: str, field_names: list) -> List[Dict]:
    query_string = "\n".join(f"{name}: SourceConnection.{name}" for name in field_names)
    query = '''
        query connectionNames($uid: string) {
            result(func: uid($uid)) { ''' + query_string + ''' }
    }
    '''
    variables = {"$uid": source_uid}
    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        try:
            result: list = res["result"]
            return result
        except KeyError:
            return list()
    else:
        return list()


def get_name_and_uid_of_catalog_from_dgraph(source_connection_xid: str) -> tuple:
    query = '''
        query connectionNames($source_connection_xid: string) {result(func: eq(dgraph.type, "SourceConnection"))
        @filter(eq(SourceConnection.xid, $source_connection_xid)) {
            uid
            name: SourceConnection.name
        }
    }
    '''
    variables = {"$source_connection_xid": source_connection_xid}
    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        try:
            return res["result"][0]["uid"], res["result"][0]["name"]
        except KeyError:
            return "", ""
    else:
        return "", ""


def check_catalog_in_dgraph(source_connection_name: str, source_connection_xid: str) -> bool:
    query = '''
        query connectionNames($source_connection_xid: string) {result(func: eq(dgraph.type, "SourceConnection"))
        @filter(eq(SourceConnection.xid, [$source_connection_xid])) {
            xid: SourceConnection.xid
            name: SourceConnection.name
        }
    }
    '''
    variables = {"$source_connection_xid": source_connection_xid}
    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        try:
            xid = res["result"][0]["xid"]
            name = res["result"][0]["name"]
            print(xid, name.lower())
            return all([(xid == source_connection_xid), (name.lower() == source_connection_name.lower())])
        except KeyError:
            return False
    else:
        return False
