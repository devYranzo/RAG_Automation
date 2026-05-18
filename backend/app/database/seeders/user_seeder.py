from sqlalchemy import select
from database.db import SessionLocal

from datetime import datetime

from models.user import User
from models.profile import Profile, Role

from core.security import hash_password

async def seed_users(session):
    stmt = select(User).where(User.email == "admin@email.com")
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()

    # User
    if not existing_user:
        admin_user = User(
            email="admin@email.com",
            hashed_password=hash_password("12345Abcde"),
            is_active=True,
            organization_id=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(admin_user)
        await session.flush()

        # Profile
        admin_profile = Profile(
            first_name="Admin",
            last_name="System",
            role=Role.Admin,
            user_id=admin_user.id,
        )

        session.add(admin_profile)

        await session.commit()
