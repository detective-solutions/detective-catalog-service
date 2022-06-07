# import standard modules
import json

# import third party modules
import pydgraph
from pydgraph import DgraphClient, AbortedError


def execute_query(client: DgraphClient, query: str, variables: dict) -> dict:
    txn = client.txn()
    try:
        res = txn.query(query, variables=variables)
        res = json.loads(res.json)

        if type(res) == dict:
            query_result = res
        else:
            query_result = {"result": ["query result was not a json object"]}
        txn.discard()
        return query_result

    except AbortedError as error:

        txn.discard()
        query_result = {"result": [error]}
        return query_result


def execute_mutation(client: DgraphClient, n_quads: str) -> bool:
    txn = client.txn()
    try:
        txn.mutate(set_nquads=n_quads)
        txn.commit()
        txn.discard()
        return True
    except pydgraph.AbortedError as error:
        print(error)
        txn.discard()
        return False


def execute_delete(client: DgraphClient, n_quad: str) -> bool:
    txn = client.txn()
    try:
        txn.mutate(del_nquads=n_quad)
        txn.commit()
        txn.discard()
        return True
    except pydgraph.AbortedError as error:
        print(error)
        txn.discard()
        return False


def execute_advanced_mutation(client: DgraphClient, query: str,
                              variables: dict, n_quad: str, execution_type: str) -> bool:
    try:
        txn = client.txn()
        if execution_type == "delete":
            mutation = txn.create_mutation(del_nquads=n_quad)
        else:
            mutation = txn.create_mutation(set_nquads=n_quad)

        request = txn.create_request(
            query=query,
            variables=variables,
            mutations=[mutation],
            commit_now=True
        )
        txn.do_request(request)
        return True
    except Exception as e:
        print(e)
        return False
