from pydantic import BaseModel, field_validator

class SendMessageToBotRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str):
        if not value.strip():
            raise ValueError("Lời thoại không được để trống")
        return value.strip()
