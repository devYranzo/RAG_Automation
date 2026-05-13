from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.user import User

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
