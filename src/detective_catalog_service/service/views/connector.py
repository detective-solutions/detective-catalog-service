# import standard modules
from copy import deepcopy

# import third party modules
from fastapi import APIRouter

# import project related modules
from detective_catalog_service.service.models.register import Register
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
    return Register.list()


@router.get("/schema/{connector_type}", responses={200: {
    "content": {
        "application/json": {
            "example": transform_model_response(Register.get("accumulo").schema())
        }
    }
}})
async def get_catalog_definition(connector_type: str):
    try:
        model = Register.get(connector_type)
        model_trans = transform_model_response(model.schema())
        for attr in model_trans["properties"]:
            if attr["required"]:
                attr["default"] = ""
        return model_trans
    except KeyError:
        return {"error": f"connector with type '{connector_type}' is not available must "
                         f"be one of {Register.list()}"}
