from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db

from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import require_admin
from services.user import user_service, user_orchestrator

router = APIRouter(prefix="/users", tags=["Users"])

# 1. Listar usuarios
@router.get("/list")
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return await user_service.get_all_users_list(db)

# 2. Crear un nuevo usuario
@router.post("/create")
async def create_new_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    existing_user = await user_service.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    return await user_orchestrator.create_user_flow(db, user_in)

# 3. Editar un usuario existente
@router.patch('/edit/{user_id}')
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return await user_service.update_user(db, user_id, user_in)

# 4. Eliminar un usuario existente
@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
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
