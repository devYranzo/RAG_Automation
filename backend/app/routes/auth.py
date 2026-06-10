from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from schemas.auth import LoginRequest, ChangePasswordRequest
from schemas.organization import CompanyRegister

from services.auth_service import authenticate_user, change_password
from services.company.company_orchestrator import register_company_flow

from core.security import require_any_user, get_current_user
from database.db import get_db
from config import settings
from models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

# REGISTER
@router.post("/register-company")
async def register_company(payload: CompanyRegister, db: Session = Depends(get_db)):
    return await register_company_flow(db=db, payload=payload)


# LOGIN
@router.post("/login")
async def login(response: Response, data: LoginRequest, db: AsyncSession = Depends(get_db)):

    token = await authenticate_user(db, data.email, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cookie_expiration = settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=cookie_expiration,
        path="/"
    )

    return {"message": "Logeado correctamente"}

@router.post("/logout", dependencies=[Depends(require_any_user)])
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/", httponly=True, samesite="lax",)
    return {"message": "Sesión cerrada"}

# CHANGE PASSWORD
@router.post("/change-password", dependencies=[Depends(require_any_user)])
async def change_user_password(
    data: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Permite que un usuario autenticado cambie su contraseña.
    Requiere proporcionar la contraseña actual como verificación.
    """
    success = await change_password(
        db=db,
        user=current_user,
        current_password=data.current_password,
        new_password=data.new_password
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="La contraseña actual es incorrecta"
        )

    return {"message": "Contraseña cambiada exitosamente"}
