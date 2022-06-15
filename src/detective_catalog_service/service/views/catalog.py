# import third party modules
from fastapi import APIRouter

# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.views.routine.delete import delete_routine
from detective_catalog_service.service.models.payload.routine import DeletePayload


router = APIRouter(
    prefix="/v1/catalog",
    tags=["catalog"],
    responses=general,
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


@router.post("/delete")
async def delete_catalog(properties: DeletePayload):
    try:
        return delete_routine(properties)
    except Exception as error:
        return {500: f"server error: {error}"}
