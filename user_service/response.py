from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    message: str

class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str
