from fastapi import APIRouter
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.models.connector.bigquery import BigQuery
from detective_catalog_service.service.views.routine.register import register_routine

router = APIRouter(
    prefix="/v1/catalog/insert",
    tags=["bigquery"],
    responses=general,
)


@router.post("/bigquery/{catalog_name}")
async def post_new_catalog(catalog_name: str, catalog_properties: BigQuery):
    try:
        return register_routine(catalog_name, catalog_properties)
    except Exception:
        return {500: "server error"}
