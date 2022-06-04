import os
import json
import requests


BASE_URL = "http://localhost:8083/v1/catalog"
header = {"Content-Type": "application/json"}


def list_catalogs():
    uri = os.path.join(BASE_URL, "catalogs")
    r = requests.get(uri, headers=header)
    if r.status_code == 200:
        return {"status": r.status_code, "body": json.loads(r.text)}
    else:
        return {"status": r.status_code, "body": [r.text]}


print(list_catalogs())