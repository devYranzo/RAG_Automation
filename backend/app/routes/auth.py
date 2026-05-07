from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth import LoginRequest, RegisterRequest, UserResponse
from services.auth_service import register_user, authenticate_user
from database.db import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])


# DB DEPENDENCY
async def get_db():
    async with SessionLocal() as session:
        yield session


# REGISTER
@router.post("/register", response_model=UserResponse)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):

    user = await register_user(db, data.email, data.password, data.first_name, data.last_name)

    return user


# LOGIN
@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):

    token = await authenticate_user(db, data.email, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token["access_token"],
        "token_type": token["token_type"]
    }
