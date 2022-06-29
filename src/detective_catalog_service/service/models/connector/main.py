# import standard modules
import inspect

# import thrid party modules
from pydantic import Field
from pydantic import BaseModel


class PropertyModel(BaseModel):
    name: str = Field(title="Name", description="The name with which this specific connection appears")

    def as_properties(self):
        raise NotImplementedError

    def setdefault(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        attributes_list = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        print(attributes_list)

