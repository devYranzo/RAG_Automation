from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.user import User
from models.profile import Profile
from models.profile import Role

from schemas.user import UserCreate, UserUpdate

from core.security import hash_password

async def get_all_users_list(db: AsyncSession):
    query = (
        select(User)
        .options(joinedload(User.profile))
    )
    result = await db.execute(query)
    users = result.scalars().all()

    return [
        {
            "id": user.id,
            "profile_id": user.profile.id if user.profile else None,
            "first_name": user.profile.first_name if user.profile else "Unknown",
            "last_name": user.profile.last_name if user.profile else "Unknown",
            "role": user.profile.role,
            "email": user.email,
            "is_active": user.is_active,
        }
        for user in users
    ]

async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_user_with_profile(db: AsyncSession, user_in: UserCreate):
    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        is_active=True,
    )
    db.add(new_user)
    await db.flush()

    # 2. Crear el Perfil
    new_profile = Profile(
        user_id=new_user.id,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        role=Role[user_in.role.capitalize()]
    )
    db.add(new_profile)

    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate):
    query = (
        select(User)
        .options(joinedload(User.profile))
        .where(User.id == user_id)
    )
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None

    update_data = user_in.model_dump(exclude_unset=True, mode='json')

    for field, value in update_data.items():
        if field == "email":
            if value != db_user.email:
                db_user.email = value

        elif field == "role":
            try:
                db_user.profile.role = Role[value.capitalize()]
            except (AttributeError, KeyError):
                continue

        else:
            if hasattr(db_user.profile, field):
                setattr(db_user.profile, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user:
        return False

    await db.delete(db_user)
    await db.commit()
    return True
