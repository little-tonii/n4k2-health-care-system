from typing import Annotated
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from user_service.model import UserModel
from user_service.request import RegisterUserRequest
from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from passlib.context import CryptContext
from user_service.response import LoginUserResponse, RegisterUserResponse
from utils.jwt import TokenClaims, create_access_token


router = APIRouter(prefix="/user", tags=["User"])

@router.post(path="/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse)
async def register_user(
    session: Annotated[AsyncSession, Depends(get_db)],
    request: RegisterUserRequest,
):
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    result = await session.execute(
        select(UserModel).where(UserModel.username == request.username)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username đã được sử dụng")
    result = await session.execute(
        select(UserModel).where(UserModel.email == request.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email đã được sử dụng")
    hashed_password = bcrypt_context.hash(request.password)
    new_user = UserModel(
        username=request.username,
        email=request.email,
        password=hashed_password,
        phone_number=request.phone_number,
        full_name=request.full_name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return RegisterUserResponse(
       message="Đăng ký thành công"
    )

@router.post(path="/login", status_code=status.HTTP_200_OK, response_model=LoginUserResponse)
async def login_user(
    session: Annotated[AsyncSession, Depends(get_db)],
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    result = await session.execute(
        select(UserModel).where(UserModel.username == login_form.username)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản hoặc mật khẩu không chính xác")
    if not bcrypt_context.verify(login_form.password, str(user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản hoặc mật khẩu không chính xác")
    access_token = create_access_token(claims=TokenClaims(id=int(str(user.id))))
    return LoginUserResponse(
        access_token=access_token,
        token_type="bearer"
    )
