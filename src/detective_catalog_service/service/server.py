# import standard modules
import setup

# import third party modules
from fastapi import FastAPI

# import project related modules
from detective_catalog_service.service.views import (
    connector,
    catalog
)
from detective_catalog_service.service.views.source import accumulo, bigquery, postgresql, cassandra

print(setup.name)
print(setup.version)

app = FastAPI(title=setup.name, version=setup.version)
app.include_router(connector.router)
app.include_router(accumulo.router)
app.include_router(postgresql.router)
app.include_router(bigquery.router)
app.include_router(cassandra.router)
app.include_router(catalog.router)
