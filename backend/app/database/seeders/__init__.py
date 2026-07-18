from database.db import SessionLocal
from database.seeders.hiring_project_seeder import seed_hiring_projects
from database.seeders.organization_seeder import seed_organizations
from database.seeders.user_seeder import seed_users

async def run_seeders():
    async with SessionLocal() as session:
        try:
            await seed_organizations(session)
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e

    async with SessionLocal() as session:
        try:
            await seed_users(session)
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e

    async with SessionLocal() as session:
        try:
            await seed_hiring_projects(session)
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e