# import standard modules
import inspect

# import thrid party modules
from pydantic import Field
from pydantic import BaseModel


class PropertyModel(BaseModel):
    name: str = Field(title="Name", description="The name with which this specific connection appears")

    def as_properties(self):
        raise NotImplementedError
