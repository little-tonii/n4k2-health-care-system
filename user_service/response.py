from typing import List
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    message: str

class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str

class UpdateProfileResponse(BaseModel):
    full_name: str
    email: str
    phone_number: str
    username: str
    id: int

class GetDoctorListItem(BaseModel):
    full_name: str
    id: int

class GetDoctorListResponse(BaseModel):
    doctors: List[GetDoctorListItem]
