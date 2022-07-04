# import standard modules
from importlib.metadata import version

# import third party modules
from fastapi import FastAPI

# import project related modules
from detective_catalog_service.service.views import (
    connector,
    catalog
)
from detective_catalog_service.service.views.source import accumulo, bigquery, postgresql, cassandra

service_name = "catalog-service"

app = FastAPI(title=service_name, version=version(service_name))
app.include_router(connector.router)
app.include_router(accumulo.router)
app.include_router(postgresql.router)
app.include_router(bigquery.router)
app.include_router(cassandra.router)
app.include_router(catalog.router)
