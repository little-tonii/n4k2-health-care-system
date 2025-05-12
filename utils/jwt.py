from datetime import datetime, timedelta, timezone
from config.environment import ACCESS_TOKEN_EXPIRES, HASH_ALGORITHM, SECRET_KEY
from jose import jwt

class TokenKey:
    ID: str = "id"
    EXPIRES: str = "exp"

class TokenClaims:
    id: int

    def __init__(self, id: int):
        self.id = id

def create_access_token(claims: TokenClaims) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRES))
    encode = { TokenKey.ID: claims.id, TokenKey.EXPIRES: expires }
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=HASH_ALGORITHM)
