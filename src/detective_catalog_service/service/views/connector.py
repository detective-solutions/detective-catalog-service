# import third party modules
from fastapi import APIRouter, HTTPException

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
    try:
        return Register.list()
    except Exception:
        raise HTTPException(status_code=500, detail="3004")


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
        for attr in model_trans.properties:
            if attr.required:
                attr.default = ""
        return model_trans
    except Exception:
        raise HTTPException(status_code=500, detail="3005")
