from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: Literal["admin", "recruiter", "viewer"] = "viewer"


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[Literal["admin", "recruiter", "viewer"]] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=64)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
