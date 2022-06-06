# import standard modules
import json

# import third party modules
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
