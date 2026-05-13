from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import SessionLocal

from models.user import User

from core.security import get_current_user
from core.security import require_admin

from services.user_service import get_all_users_list

router = APIRouter(prefix="/users", tags=["Users"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/list", dependencies=[Depends(require_admin)])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users_list(db)
