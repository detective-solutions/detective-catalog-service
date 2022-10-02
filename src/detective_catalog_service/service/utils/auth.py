
# import standard modules
import jwt
import time
import json
import base64

# import third party modules
import requests

# import project related modules
from detective_catalog_service.service.models.response.response_auth import LoginResponse
from detective_catalog_service.service.models.payload.payload_auth import LoginPayload, Token
from detective_catalog_service.settings import AUTH_SERVER, JWT_SECRET, JWT_ALGORITHM


def login(request: LoginPayload) -> LoginResponse:
    """
    login to detective with email and password
    :param request: body with email and password attributes
    :return: data with status code, access token and refresh token
    """

    payload = {
        "email": request.email,
        "password": request.password
    }
    r = requests.post(
        f"http://{AUTH_SERVER}/v1/auth/login", data=payload)
    data = json.loads(r.text)

    return LoginResponse(
        status_code=r.status_code,
        accessTokenSecret=data.get("access_token", f"{data}"),
        refreshTokenSecret=data.get("refresh_token", "")
    )


def token_validate(token: Token) -> bool:
    """
    function to validate a detective authentication token
    :param token: token string
    :return: True if valid, False otherwise
    """
    secret: str = JWT_SECRET or ""
    algorithm: str = JWT_ALGORITHM or ""
    jwt_options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }

    decoded_token = jwt.decode(
        token.access_token,
        base64.b64decode(secret).decode('utf-8'),
        algorithms=[algorithm],
        options=jwt_options
    )

    try:
        return True if decoded_token["exp"] >= time.time() else False
    except KeyError:
        return False


def tenant_from_token(token: Token) -> str:
    """
    extract a tenant from given token
    :param token: token string
    :return: tenant id in uuid format
    """
    secret: str = JWT_SECRET or ""
    algorithm: str = JWT_ALGORITHM or ""
    jwt_options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }

    decoded_token = jwt.decode(
        token.access_token,
        base64.b64decode(secret).decode('utf-8'),
        algorithms=[algorithm],
        options=jwt_options
    )
    try:
        return decoded_token.get("tenantId", "")
    except KeyError:
        return ""
