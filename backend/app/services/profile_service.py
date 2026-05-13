from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.user import User

async def get_profile_data(db: AsyncSession, current_user: User):
    query = (
        select(User)
        .options(joinedload(User.profile))
        .where(User.id == current_user.id)
    )
    result = await db.execute(query)
    user = result.scalar_one()

    return {
        "profile_id": user.profile.id if user.profile else None,
        "first_name": user.profile.first_name if user.profile else "Unknow",
        "last_name": user.profile.last_name if user.profile else "Unknow",
        "role": user.profile.role if user.profile else "viewer",
        "email": user.email,
        "is_active": user.is_active,
    }
