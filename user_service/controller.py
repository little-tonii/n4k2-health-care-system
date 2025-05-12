from typing import Annotated
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from config.security import verify_access_token
from user_service.model import UserModel
from user_service.request import RegisterUserRequest, UpdateProfileUserRequest
from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from passlib.context import CryptContext
from user_service.response import LoginUserResponse, RegisterUserResponse, UpdateProfileResponse
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

@router.patch(path="/profile", status_code=status.HTTP_200_OK, response_model=UpdateProfileResponse)
async def update_profile(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    session: Annotated[AsyncSession, Depends(get_db)],
    update_request: UpdateProfileUserRequest,
):
    result = await session.execute(
        select(UserModel).where(UserModel.id == claims.id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
    if update_request.email and update_request.email != user.email:
        result = await session.execute(
            select(UserModel).where(UserModel.email == update_request.email)
        )
        existing_email_user = result.scalar_one_or_none()
        if existing_email_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email đã được sử dụng")
    if update_request.full_name is not None:
        user.full_name = update_request.full_name # type: ignore
    if update_request.email is not None:
        user.email = update_request.email # type: ignore
    if update_request.phone_number is not None:
        user.phone_number = update_request.phone_number # type: ignore
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UpdateProfileResponse(
        full_name=user.full_name, # type: ignore
        email=user.email, # type: ignore
        phone_number=user.phone_number, # type: ignore
        username=user.username, # type: ignore
        id=user.id # type: ignore
    )
