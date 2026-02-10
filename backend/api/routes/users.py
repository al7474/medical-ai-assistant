"""
User endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List

from models import User
from schemas.user import UserCreate, UserRead
from api.deps import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_user


@router.get("/", response_model=List[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    """List all users"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
