# import third party modules
from fastapi import APIRouter

# import project related modules
from detective_catalog_service.service.models.register import register
from detective_catalog_service.service.views.responses.codes import general

router = APIRouter(
    prefix="/v1/catalog/connector",
    tags=["connector"],
    responses=general,
)


@router.get("/list", responses={200: {
    "content": {
        "application/json": {
            "example": {"types": ["postgres", "sqlserver", "models"]}
        }
    }
}})
async def list_catalog():
    return {"types": list(register.keys())}


@router.get("/schema/{connector_type}", responses={200: {
    "content": {
        "application/json": {
            "example": register["accumulo"].schema()
        }
    }
}})
async def get_catalog_definition(connector_type: str):
    try:
        model = register[connector_type]
        return model.schema()
    except KeyError:
        return {"error": f"connector with type '{connector_type}' is not available must "
                         f"be one of {list(register.keys())}"}
