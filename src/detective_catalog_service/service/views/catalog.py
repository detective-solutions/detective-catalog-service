# import third party modules
from fastapi import APIRouter

# import project related modules
from detective_catalog_service.trino.api import TrinoOperation
from detective_catalog_service.service.models.register import register
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.views.routine.delete import delete_routine
from detective_catalog_service.service.models.payload.routine import DeletePayload
from detective_catalog_service.service.models.utils import transform_model_response
from detective_catalog_service.database.queries import get_source_connection_values, get_source_connection_id_and_type_by_xid


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


@router.get("/schema/{source_connection_xid}")
async def get_catalog_definition(source_id: str):
    try:
        source = get_source_connection_id_and_type_by_xid(source_id)
        schema_type = register[source.get("connectorName")]
        schema = schema_type.schema()
        source_values = get_source_connection_values(source["uid"], list(schema["properties"].keys()))

        print(source_values)
        for key, value in source_values[0].items():
            schema["properties"][key]["default"] = value
        return transform_model_response(schema)
    except KeyError as error:
        return {"error": f"{error}"}