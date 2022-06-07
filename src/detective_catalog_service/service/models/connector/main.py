# import thrid party modules
from pydantic import BaseModel


class PropertyModel(BaseModel):
    def as_properties(self):
        raise NotImplementedError
