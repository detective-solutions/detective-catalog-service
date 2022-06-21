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
    try:
        return register_routine(source_connection_properties)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"5000: {error}")


@router.post("/update/{source_connection_xid}")
async def update_existing_catalog(source_connection_xid: str, source_connection_properties: PostgreSQL):
    try:
        payload = UpdatePayload(
            source_connection_xid=source_connection_xid,
            source_connection_properties=source_connection_properties
        )
        return update_routine(payload)
    except Exception:
        raise HTTPException(status_code=500, detail="5000")
