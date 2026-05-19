from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import settings
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.db import SessionLocal
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Utilidades de Password ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- Gestión de JWT ---
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire_datetime = datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)

    expire_timestamp = int(expire_datetime.timestamp())

    to_encode.update({"exp": expire_timestamp})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# --- Dependencia para obtener el usuario actual ---
async def get_current_user(
    access_token: str | None = Cookie(None)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales o la sesión ha expirado",
    )

    if not access_token:
        raise credentials_exception

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    async with SessionLocal() as session:
        query = (
            select(User)
            .options(joinedload(User.profile))
            .where(User.email == email)
        )
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = [role.lower() for role in allowed_roles]

    def __call__(self, current_user: User = Depends(get_current_user)):
        user_role = ""
        if current_user.profile and current_user.profile.role:
            if hasattr(current_user.profile.role, 'name'):
                user_role = current_user.profile.role.name.lower()
            else:
                user_role = str(current_user.profile.role).lower()

        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes."
            )
        return current_user

require_admin = RoleChecker(["admin"])
require_recruiter = RoleChecker(["admin", "recruiter"])
require_any_user = RoleChecker(["admin", "recruiter", "viewer"])
