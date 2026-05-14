from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import SessionLocal

from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import require_admin, get_current_user
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

async def get_db():
    async with SessionLocal() as session:
        yield session

# Get user list
@router.get("/list", dependencies=[Depends(require_admin)])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_all_users_list(db)

# Create a new user
@router.post("/create", dependencies=[Depends(require_admin)])
async def create_new_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await user_service.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    return await user_service.create_user_with_profile(db, user_in)

# Edit an existing user
@router.patch('/edit/{user_id}', dependencies=[Depends(require_admin)])
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await user_service.update_user(db, user_id, user_in)

# Delete an exising user
@router.delete("/delete/{user_id}", dependencies=[Depends(require_admin)])
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # PROTECCIÓN: No permitir auto-borrado
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="No puedes eliminar tu propia cuenta de administrador"
        )

    success = await user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario eliminado correctamente"}
