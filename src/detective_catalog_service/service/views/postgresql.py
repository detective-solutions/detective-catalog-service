# import third party modules
from fastapi import APIRouter

# import project related modules
from detective_catalog_service.service.models.postgresql import PostgreSQL
from detective_catalog_service.service.views.routine.register import register_routine


router = APIRouter(
    prefix="/v1/catalog/insert",
    tags=["postgresql"],
    responses={404: {"description": "Not found"}},
)


@router.post("/postgresql/{catalog_name}")
async def post_new_catalog(catalog_name: str, catalog_properties: PostgreSQL):
    try:
        return register_routine(catalog_name, catalog_properties)
    except Exception:
        return {500: "properties provided invalid"}