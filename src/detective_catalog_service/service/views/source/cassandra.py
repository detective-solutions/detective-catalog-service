from fastapi import APIRouter
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.models.connector.cassandra import Cassandra
from detective_catalog_service.service.views.routine.register import register_routine

router = APIRouter(
    prefix="/v1/catalog/insert",
    tags=["cassandra"],
    responses=general,
)


@router.post("/cassandra/{catalog_name}")
async def post_new_catalog(catalog_name: str, catalog_properties: Cassandra):
    try:
        return register_routine(catalog_name, catalog_properties)
    except Exception:
        return {500: "server error"}
