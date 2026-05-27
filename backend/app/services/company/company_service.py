from sqlalchemy import select
from models.organization import Organization
from models.profile import Profile
from models.user import User
from core.security import hash_password


async def create_company(db, payload):

    # Organization
    new_org = Organization(name=payload.company_name)
    db.add(new_org)
    await db.flush()

    # User admin
    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        organization_id=new_org.id
    )
    db.add(new_user)
    await db.flush()

    # Profile
    new_profile = Profile(
        user_id=new_user.id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        role="Admin"
    )
    db.add(new_profile)

    await db.commit()

    return {
        "organization": new_org,
        "user": new_user,
        "profile": new_profile
    }

async def delete_company(db, org_id: int):

    result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )

    org = result.scalar_one_or_none()

    if not org:
        return False

    await db.delete(org)
    await db.commit()

    return True
