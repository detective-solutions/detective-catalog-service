# import third party modules
from pydantic import BaseModel


class LoginResponse(BaseModel):
    status_code: int = 404
    accessTokenSecret: str = ""
    refreshTokenSecret: str = ""
