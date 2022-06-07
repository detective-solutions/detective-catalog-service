# import standard modules
import logging
from uuid import UUID

# import third party modules
from pydantic import BaseModel, validator, ValidationError


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
