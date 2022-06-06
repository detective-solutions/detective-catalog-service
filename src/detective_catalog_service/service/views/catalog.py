# import third party modules
from fastapi import APIRouter

# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.models.register import register

router = APIRouter(
    prefix="/v1/catalog",
    tags=["catalog"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", responses={200: {
    "content": {
        "application/json": {
            "example": {"types": ["catalog1", "catalog2"]}
        }
    }
}})
async def list_catalog_names():
    return TrinoOperation.list_catalog()
