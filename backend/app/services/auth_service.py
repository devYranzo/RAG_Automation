from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status

from models.user import User

from core.security import verify_password, create_access_token, hash_password

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(User)
        .options(joinedload(User.profile))
        .where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password): # type: ignore
        return None

    return create_access_token({"sub": user.email, "role": user.profile.role.value,
        "organization_id": user.organization_id,})


async def change_password(db: AsyncSession, user: User, current_password: str, new_password: str) -> bool:
    """
    Cambia la contraseña del usuario después de verificar la contraseña actual.

    Args:
        db: Sesión de base de datos
        user: Usuario actual
        current_password: Contraseña actual para verificación
        new_password: Nueva contraseña a establecer

    Returns:
        True si se cambió exitosamente, False si la contraseña actual es incorrecta
    """
    if not verify_password(current_password, user.hashed_password):
        return False

    # Obtener el usuario nuevamente de la base de datos para asegurar que está en la sesión actual
    result = await db.execute(
        select(User).where(User.id == user.id)
    )
    db_user = result.scalar_one_or_none()

    if not db_user:
        return False

    db_user.hashed_password = hash_password(new_password)
    db.add(db_user)
    await db.commit()
    return True
