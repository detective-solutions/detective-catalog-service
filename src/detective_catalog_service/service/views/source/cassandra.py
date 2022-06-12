from fastapi import APIRouter
from detective_catalog_service.service.views.responses.codes import general
from detective_catalog_service.service.views.routine.update import update_routine
from detective_catalog_service.service.models.payload.routine import UpdatePayload
from detective_catalog_service.service.models.connector.cassandra import Cassandra
from detective_catalog_service.service.views.routine.register import register_routine

router = APIRouter(
    prefix="/v1/catalog/cassandra",
    tags=["cassandra"],
    responses=general,
)


@router.post("/insert/{source_connection_name}")
async def post_new_catalog(source_connection_name: str, source_connection_properties: Cassandra):
    try:
        return register_routine(source_connection_name, source_connection_properties)
    except Exception:
        return {500: "server error"}


@router.post("/update/{source_connection_xid}")
async def update_existing_catalog(source_connection_xid: str, source_connection_properties: Cassandra):
    try:
        payload = UpdatePayload(
            source_connection_xid=source_connection_xid,
            source_connection_properties=source_connection_properties
        )
        return update_routine(payload)
    except Exception:
        return {500: "server error"}
