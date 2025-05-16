from pydantic import BaseModel


class SendMessageToBotResponse(BaseModel):
    message: str
