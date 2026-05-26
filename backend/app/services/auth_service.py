from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status

from models.user import User

from core.security import verify_password, create_access_token

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(User)
        .options(joinedload(User.profile))
        .where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password): # type: ignore
        return None

    return create_access_token({"sub": user.email, "role": user.profile.role.value,
        "organization_id": user.organization_id,})
