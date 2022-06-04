import os
import json
import requests

BASE_URL = "http://localhost:8083/v1/catalog"
header = {"Content-Type": "application/json"}
payload = {
    "connector.name": "postgresql",
    "connection-url": "jdbc:postgresql://dumbo.db.elephantsql.com:5432/fkutbowf",
    "connection-user": "fkutbowf",
    "connection-password": "6f8QOboUReqfLJ17mukRAyWBEME6xolU"
}


def register_catalog(name, properties):
    uri = os.path.join(BASE_URL, f"register?name={name}")
    r = requests.post(uri, headers=header, data=json.dumps(properties))
    if r.status_code == 204:
        return {"status": r.status_code, "body": "success"}
    else:
        return {"status": r.status_code, "body": "fail"}


print(register_catalog(name="elephant", properties=payload))
