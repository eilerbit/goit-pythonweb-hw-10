﻿from fastapi import APIRouter, Depends, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.schemas import User
from src.services.auth import get_current_user
from src.conf.config import config

from src.services.upload_file import UploadFileService
from src.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)

@router.get(
    "/me",
    response_model=User,
    description="Return the current user. Maximum 10 requests per minute."
)
@limiter.limit("10/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user

@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    uploader = UploadFileService(
        cloud_name=config.CLD_NAME,
        api_key=str(config.CLD_API_KEY),
        api_secret=config.CLD_API_SECRET
    )
    avatar_url = uploader.upload_file(file, user.username)

    user_service = UserService(db)
    updated_user = await user_service.update_avatar_url(user.email, avatar_url)

    return updated_user