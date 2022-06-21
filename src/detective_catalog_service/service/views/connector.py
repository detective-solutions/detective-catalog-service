# import third party modules
from fastapi import APIRouter

# import project related modules
from detective_catalog_service.service.models.register import register
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.models.utils import transform_model_response

router = APIRouter(
    prefix="/v1/catalog/connector",
    tags=["connector"],
    responses=general,
)


@router.get("/list", responses={200: {
    "content": {
        "application/json": {
            "example": {"types": [{"connectorName": "postgresql", "displayName": "PostgreSQL"}]}
        }
    }
}})
async def list_catalog():
    result = [
        {"connectorName": key, "displayName": value.__name__}
        for key, value in register.items()
    ]
    return result


@router.get("/schema/{connector_type}", responses={200: {
    "content": {
        "application/json": {
            "example": transform_model_response(register["accumulo"].schema())
        }
    }
}})
async def get_catalog_definition(connector_type: str):
    try:
        model = register[connector_type]
        model = transform_model_response(model.schema())
        return model
    except KeyError:
        return {"error": f"connector with type '{connector_type}' is not available must "
                         f"be one of {list(register.keys())}"}
