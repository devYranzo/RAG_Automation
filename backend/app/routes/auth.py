from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth import LoginRequest, RegisterRequest, UserResponse
from services.auth_service import register_user, authenticate_user
from core.security import require_any_user
from database.db import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])


# DB DEPENDENCY
async def get_db():
    async with SessionLocal() as session:
        yield session


# REGISTER
@router.post("/register", response_model=UserResponse, dependencies=[Depends(require_any_user)])
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):

    user = await register_user(db, data.email, data.password, data.first_name, data.last_name)

    return user


# LOGIN
@router.post("/login")
async def login(response: Response, data: LoginRequest, db: AsyncSession = Depends(get_db), dependencies=[Depends(require_any_user)]):

    token = await authenticate_user(db, data.email, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
        path="/"
    )

    return {"message": "Logeado correctamente"}

@router.post("/logout", dependencies=[Depends(require_any_user)])
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/", httponly=True, samesite="lax",)
    return {"message": "Sesión cerrada"}
