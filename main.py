from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from config.database import init_db
from config.exception_handler import process_global_exception, process_http_exception, process_validation_error
from user_service import controller as user_controller
from chatbot_service import controller as chatbot_controller
from patient_service import controller as patient_controller

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Health Care System", lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(chatbot_controller.router)
app.include_router(patient_controller.router)

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return process_http_exception(exc)

@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return process_validation_error(exc)

@app.exception_handler(RequestValidationError)
def request_validation_error_handler(request: Request, exc: RequestValidationError):
    return process_validation_error(exc)

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    return process_global_exception(exc)
