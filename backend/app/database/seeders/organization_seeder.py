from sqlalchemy import select
from database.db import SessionLocal
from models.organization import Organization

async def seed_organizations(session):
    stmt = select(Organization).filter(Organization.id == 1)
    result = await session.execute(stmt)
    existing_org = result.scalar_one_or_none()

    # 2. Si no existe, la creamos con ID = 1
    if not existing_org:
        default_org = Organization(
            id=1,
            name="Default Organization"
            # Si añadiste token_pool_limit en tu modelo, puedes ponerlo aquí:
            # token_pool_limit=5000000
        )
        session.add(default_org)
        await session.flush()
