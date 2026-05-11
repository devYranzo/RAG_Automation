from .user_seeder import seed_users

async def run_seeders():
    await seed_users()
