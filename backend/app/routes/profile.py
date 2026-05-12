from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import SessionLocal
from schemas.profile import ProfileResponse
from services.profile_service import get_profile_data
from core.security import get_current_user # Tu función que valida el JWT
from models.user import User

router = APIRouter(prefix="/profile", tags=["Profile"])

# Dependencia de DB
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get('/me', response_model=ProfileResponse)
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) # Usa la nueva dependencia
):
    return await get_profile_data(db, current_user)
