# import standard modules
import logging
from uuid import UUID

# import third party modules
from pydantic import BaseModel, validator, ValidationError

# import project related modules
from detective_catalog_service.service.models.connector.main import PropertyModel


class DeletePayload(BaseModel):
    source_connection_xid: str
    source_connection_name: str

    @validator('source_connection_xid')
    def check_for_valid_uuid(cls, uuid_string: str):
        try:
            UUID(uuid_string)
            return uuid_string
        except ValueError:
            logging.error(f"source connection delete request for {uuid_string} was invalid")
            raise ValidationError


class UpdatePayload(BaseModel):
    source_connection_xid: str
    source_connection_properties: PropertyModel
