from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth import LoginRequest, RegisterRequest
from services.auth_service import register_user, authenticate_user
from database.db import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])


# DB DEPENDENCY
async def get_db():
    async with SessionLocal() as session:
        yield session


# REGISTER
@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):

    user = await register_user(db, data.username, data.password)

    return {"message": "User created", "user_id": user.id}


# LOGIN
@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):

    token = await authenticate_user(db, data.username, data.password)

    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }
