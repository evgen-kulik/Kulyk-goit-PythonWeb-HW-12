from typing import List

from fastapi_limiter.depends import RateLimiter  # для обмеження кількості запитів

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserModel, UserResponse
from src.repository import users as repository_users
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=List[UserResponse],
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    users = await repository_users.get_users(skip, limit, db)
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    user = await repository_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# Тепер контакт додається тільки під час SignUp
# @router.post("/", response_model=UserResponse)
# async def create_user_by_user(body: UserModel, db: Session = Depends(get_db)):
#     return await repository_users.create_user(body, db)
# ---------------


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def update_user(
    body: UserModel,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    user = await repository_users.update_user(user_id, body, db, current_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    user = await repository_users.remove_user(user_id, db, current_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get(
    "/user_name/",
    response_model=UserResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def find_user_by_name(
    user_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    if user_name:
        user = await repository_users.find_user_by_name(user_name, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user


@router.get(
    "/user_last_name/",
    response_model=UserResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def find_user_by_last_name(
    user_last_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    if user_last_name:
        user = await repository_users.find_user_by_last_name(user_last_name, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user


@router.get(
    "/user_email/",
    response_model=UserResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def find_user_by_email(
    user_email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    if user_email:
        user = await repository_users.find_user_by_email(user_email, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user


@router.get(
    "/next_7_days_birthdays/",
    response_model=List[UserResponse],
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def find_next_7_days_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    user = await repository_users.find_next_7_days_birthdays(db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No birthdays in next 7 days"
        )
    return user
