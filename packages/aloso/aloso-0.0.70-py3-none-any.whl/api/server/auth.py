from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

import config

api_key_header = APIKeyHeader(name="api_key", auto_error=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")


def check_api_key(api_key: str = Depends(oauth2_scheme)):
    if api_key != config.key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return api_key
