from typing import Annotated
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
import google.generativeai as genai
from starlette import status

from chatbot_service.request import SendMessageToBotRequest
from chatbot_service.response import SendMessageToBotResponse
from config.environment import GEMINI_TOKEN
from config.security import verify_access_token
from utils.jwt import TokenClaims


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


genai.configure(api_key=GEMINI_TOKEN) # pyright: ignore[reportPrivateImportUsage]
model = genai.GenerativeModel(model_name='gemini-2.0-flash') # pyright: ignore[reportPrivateImportUsage]

@router.post(path="", status_code=status.HTTP_200_OK,response_model=SendMessageToBotResponse)
async def send_message(
    _: Annotated[TokenClaims, Depends(verify_access_token)],
    request: SendMessageToBotRequest,
):
    response = model.generate_content(request.message)
    if response and response.text:
        chatbot_reply = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể phản hồi"
        )
    return SendMessageToBotResponse(message=chatbot_reply)
