# import standard modules
import os
import json
import requests

# import project related modules
from detective_catalog_service.settings import TRINO_SERVER


class TrinoOperation:

    ENDPOINT = f"http://{TRINO_SERVER}/v1/catalog"
    HEADER = {"Content-Type": "application/json"}

    @classmethod
    def register_catalog(cls, name: str, properties: dict) -> bool:
        uri = os.path.join(cls.ENDPOINT, f"register?name={name}")
        r = requests.post(uri, headers=cls.HEADER, data=json.dumps(properties))
        if r.status_code == 204:
            return True
        else:
            print("FAIL WITH: ", r.status_code, r.text)
            return False

    @classmethod
    def list_catalog(cls) -> dict:
        uri = os.path.join(cls.ENDPOINT, "catalogs")
        r = requests.get(uri, headers=cls.HEADER)
        if r.status_code == 200:
            return {"status": r.status_code, "body": json.loads(r.text)}
        else:
            return {"status": r.status_code, "body": [r.text, uri]}

    @classmethod
    def update_catalog(cls, name: str, properties: dict) -> bool:
        uri = os.path.join(cls.ENDPOINT, f"update?name={name}")
        r = requests.post(uri, headers=cls.HEADER, data=json.dumps(properties))
        if r.status_code == 204:
            return True
        else:
            return False

    @classmethod
    def delete_catalog(cls, name: str):
        uri = os.path.join(cls.ENDPOINT, f"remove?name={name}")
        r = requests.post(uri, headers=cls.HEADER)
        if r.status_code == 204:
            return True
        else:
            return False

    @classmethod
    def check_catalog_by_name_in_trino(cls, catalog_name: str) -> bool:
        catalogs = cls.list_catalog()
        print(catalogs)
        if catalogs["status"] == 200:
            if catalog_name in catalogs["body"]:
                return True
            else:
                return False
        else:
            return False
