from pydantic import BaseModel, field_validator
from email_validator import validate_email, EmailNotValidError
import re


class RegisterUserRequest(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        if not value.strip():
            raise ValueError("Username không được để trống")
        return value.strip().lower()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        if not value.strip():
            raise ValueError("Email không được để trống")
        try:
            email_infor = validate_email(value, check_deliverability=True)
            return email_infor.normalized.lower()
        except EmailNotValidError:
            raise ValueError(f"Email {value} không hợp lệ")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not value or len(value) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str):
        # Vietnamese phone number: starts with 0, 84, or +84, followed by 9 digits (total 10 or 11 digits)
        pattern = r"^(0|\+84|84)(3[2-9]|5[6|8|9]|7[0|6-9]|8[1-5]|9[0-9])[0-9]{7}$"
        normalized = value.strip().replace(" ", "")
        if not re.match(pattern, normalized):
            raise ValueError("Số điện thoại không hợp lệ")
        return normalized
