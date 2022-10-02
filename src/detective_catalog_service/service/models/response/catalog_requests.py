# import standard modules
from typing import Optional, List

# import third party modules
from pydantic import BaseModel


class RoutineResponse(BaseModel):
    success: bool = False
    description: str = ""
    error: Optional[str]


class RegisterResponse(BaseModel):
    error: Optional[str]


class CatalogProperty(BaseModel):
    propertyName: str
    displayName: str
    description: str
    default: str
    type: str
    required: bool


class CatalogDefinitionResponse(BaseModel):
    connectorType: str
    properties: List[CatalogProperty]
