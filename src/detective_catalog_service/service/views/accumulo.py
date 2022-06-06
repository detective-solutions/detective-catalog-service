from fastapi import APIRouter
from detective_catalog_service.service.models.accumulo import Accumulo
from detective_catalog_service.service.views.routine.register import register_routine

router = APIRouter(
    prefix="/v1/catalog/insert",
    tags=["accumulo"],
    responses={404: {"description": "Not found"}},
)


@router.post("/accumulo/{catalog_name}")
async def post_new_catalog(catalog_name: str, catalog_properties: Accumulo):
    try:
        return register_routine(catalog_name, catalog_properties)
    except Exception:
        return {500: "properties provided invalid"}
