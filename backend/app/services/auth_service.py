from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import User
from core.security import verify_password, create_access_token, hash_password


async def register_user(db: AsyncSession, username: str, password: str):

    user = User(
        username=username,
        hashed_password=hash_password(password)
    )

    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(db: AsyncSession, username: str, password: str):

    result = await db.execute(
        select(User).where(User.username == username)
    )

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.hashed_password): # type: ignore
        return None

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
