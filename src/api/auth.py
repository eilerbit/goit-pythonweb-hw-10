from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import UserCreate, Token, User
from src.services.auth import create_access_token, Hash
from src.services.users import UserService
from src.database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)

    if await user_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач із таким email вже існує.",
        )

    if await user_service.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач із таким username вже існує.",
        )

    hashed_pw = Hash().get_password_hash(user_data.password)
    user_data.password = hashed_pw

    new_user = await user_service.create_user(user_data)
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Неправильний логін або пароль")

    if not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неправильний логін або пароль")

    access_token = await create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
