# import third party modules
from fastapi import APIRouter, HTTPException

# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.models.register import Register
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.views.routine.delete import delete_routine
from detective_catalog_service.service.models.payload.routine import DeletePayload
from detective_catalog_service.service.models.utils import transform_model_response
from detective_catalog_service.service.models.response.catalog_requests import (
    RoutineResponse,
    CatalogDefinitionResponse
)
from detective_catalog_service.database.queries import (
    get_source_connection_values,
    get_source_connection_id_and_type_by_xid
)


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
    try:
        return TrinoOperation.list_catalog()
    except Exception:
        raise HTTPException(status_code=500, detail="3000")


@router.post("/delete", response_model=RoutineResponse)
async def delete_catalog(properties: DeletePayload):
    execution_status = delete_routine(properties)
    if execution_status.success:
        return execution_status
    else:
        raise HTTPException(status_code=500, detail=execution_status.error)


@router.get("/schema/{source_connection_xid}", response_model=CatalogDefinitionResponse)
async def get_catalog_definition(source_connection_xid: str):
    try:
        source = get_source_connection_id_and_type_by_xid(source_connection_xid)
        schema_type = Register.get(source.get("connectorName", ""))
        schema = schema_type.schema()
        source_values = get_source_connection_values(source["uid"], list(schema["properties"].keys()))

        for key, value in source_values[0].items():
            schema["properties"][key]["default"] = value

        return transform_model_response(schema)

    except Exception:
        raise HTTPException(status_code=500, detail="3003")
