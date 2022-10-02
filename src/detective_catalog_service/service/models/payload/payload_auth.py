# import third party modules
from pydantic import BaseModel, EmailStr


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
