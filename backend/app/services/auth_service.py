from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status

from models.user import User
from models.organization import Organization
from models.profile import Profile

from schemas.organization import CompanyRegister

from core.security import verify_password, create_access_token, hash_password

async def register_new_company(db: AsyncSession, payload: CompanyRegister):
    # Verificar si la empresa ya existe
    result = await db.execute(
        select(Organization).where(Organization.name == payload.company_name)
    )
    existing_org = result.scalar_one_or_none()

    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de la empresa ya está registrado."
        )

    # Verificar si el email ya existe
    user_result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    existing_user = user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está en uso."
        )

    try:
        # Crear la Organización
        new_org = Organization(name=payload.company_name)
        db.add(new_org)
        await db.flush()

        # Crear el Usuario base
        hashed_pwd = hash_password(payload.password)
        new_user = User(
            email=payload.email,
            hashed_password=hashed_pwd,
            organization_id=new_org.id
        )
        db.add(new_user)
        await db.flush()

        # Crear el Profile
        new_profile = Profile(
            user_id=new_user.id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            role="Admin",
        )
        db.add(new_profile)

        await db.commit()

        return {"message": "Organización, usuario administrador y perfil creados con éxito"}

    except Exception as e:
        await db.rollback()
        print(f"Error en AuthService.register_new_company: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear la cuenta de organización."
        )

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
