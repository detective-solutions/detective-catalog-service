# import standard modules

# import third party modules
from fastapi import FastAPI

# import project related modules
from detective_catalog_service.service.views import (
    connector,
    catalog
)
from detective_catalog_service.service.views.source import accumulo, bigquery, postgresql

app = FastAPI(title="detective-catalog-service", version="0.0.1")
app.include_router(connector.router)
app.include_router(accumulo.router)
app.include_router(postgresql.router)
app.include_router(bigquery.router)
app.include_router(catalog.router)
