from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from fastapi import HTTPException, status

from models.user import User
from models.organization import Organization

from schemas.organization import CompanyRegister

from core.security import verify_password, create_access_token, hash_password


async def register_new_company(db: Session, payload: CompanyRegister):
    # 1. Verificar si la empresa ya existe
    existing_org = db.query(Organization).filter(Organization.name == payload.company_name).first()
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de la empresa ya está registrado."
        )

    # 2. Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está en uso."
        )

    try:
        # 3. Crear primero la Organización
        new_org = Organization(name=payload.company_name)
        db.add(new_org)
        db.flush()

        # 4. Crear el Usuario Administrador asignándole esa organización
        hashed_pwd = hash_password(payload.password)
        new_user = User(
            email=payload.email,
            hashed_password=hashed_pwd,
            role="admin",
            organization_id=new_org.id
        )
        db.add(new_user)
        db.commit()

        return {"message": "Organización y usuario creados con éxito"}

    except Exception as e:
        db.rollback()
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
