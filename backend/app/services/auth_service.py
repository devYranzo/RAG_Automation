from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import User
from core.security import verify_password, create_access_token, hash_password


async def register_user(db: AsyncSession, email: str, password: str, first_name: str | None = None, last_name: str | None = None):

    user = User(
        email=email,
        hashed_password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
    )

    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):

    result = await db.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.hashed_password): # type: ignore
        return None

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
