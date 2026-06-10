from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=64)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
