from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = "viewer"

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # Solo para admin: restablecer contraseña de otro usuario

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
