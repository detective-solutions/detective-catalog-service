# import standard modules
import os
import json
import requests

# import project related modules
from detective_catalog_service.settings import TRINO_SERVER
from detective_catalog_service.service.event import post_event, subscribe


class CatalogOperation:

    ENDPOINT = "v1/catalog"
    HEADER = {"Content-Type": "application/json"}

    @classmethod
    def register_catalog(cls, name, properties) -> None:
        uri = os.path.join(TRINO_SERVER, cls.ENDPOINT, f"register?name={name}")
        r = requests.post(uri, headers=cls.HEADER, data=json.dumps(properties))
        if r.status_code == 204:
            post_event("register_success", {"status": r.status_code, "body": "success"})
        else:
            post_event("register_error", {"status": r.status_code, "body": "fail"})

    @classmethod
    def list_catalog(cls):
        uri = os.path.join(TRINO_SERVER, cls.ENDPOINT, "catalogs")
        r = requests.get(uri, headers=cls.HEADER)
        if r.status_code == 200:
            post_event("list_success", {"status": r.status_code, "body": json.loads(r.text)})
        else:
            post_event("list_error", {"status": r.status_code, "body": [r.text]})

    @classmethod
    def update_catalog(cls):
        pass

    @classmethod
    def delete_catalog(cls):
        pass


def setup_catalog_events():
    subscribe("register_catalog", CatalogOperation.register_catalog)
    subscribe("list_catalog", CatalogOperation.list_catalog)