from jose import JWTError, jwt
from starlette import status
from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from config.environment import HASH_ALGORITHM, SECRET_KEY
from utils.jwt import TokenClaims, TokenKey


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/login')

async def verify_access_token(
    request: Request,
    token: Annotated[str, Depends(oauth2_bearer)],
) -> TokenClaims:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: int | None = payload.get(TokenKey.ID)
        role: str | None = payload.get(TokenKey.ROLE)
        expires: int | None = payload.get(TokenKey.EXPIRES)
        if user_id is None or role is None or expires is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if datetime.now(timezone.utc).timestamp() > expires:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        claims = TokenClaims(id=user_id, role=role)
        request.state.claims = claims
        return claims
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
