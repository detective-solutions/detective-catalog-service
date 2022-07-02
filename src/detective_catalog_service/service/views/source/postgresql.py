# import third party modules
from fastapi import APIRouter, HTTPException

# import project related modules
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.views.routine.update import update_routine
from detective_catalog_service.service.models.payload.routine import UpdatePayload
from detective_catalog_service.service.models.connector.postgresql import PostgreSQL
from detective_catalog_service.service.views.routine.register import register_routine


router = APIRouter(
    prefix="/v1/catalog/postgresql",
    tags=["postgresql"],
    responses=general,
)


@router.post("/insert")
async def post_new_catalog(source_connection_properties: PostgreSQL):
    result = register_routine(source_connection_properties)
    if list(result.keys())[0] == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))
    else:
        return result


@router.post("/update/{source_connection_xid}")
async def update_existing_catalog(source_connection_xid: str, source_connection_properties: PostgreSQL):
    payload = UpdatePayload(
        source_connection_xid=source_connection_xid,
        source_connection_properties=source_connection_properties
    )
    result = update_routine(payload)
    if list(result.keys())[0] == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))
    else:
        return result
