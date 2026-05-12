from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
    expire = datetime.now() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# --- Dependencia para obtener el usuario actual ---
async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")

        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Buscamos al usuario en la DB usando el email extraído del token
    async with SessionLocal() as session:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception
        return user
