from pydantic import BaseModel, EmailStr, Field

class CompanyRegister(BaseModel):
  # Company Info
  company_name: str = Field(
      ...,
      min_length=2,
      max_length=100,
      description="Company name which will manage this workspace"
  )

  # Admin Account Info
  email: EmailStr = Field(
      ...,
      description="Email del usuario que actuará como Super Admin de la organización"
  )
  password: str = Field(
      ...,
      min_length=8,
      max_length=64,
      description="Contraseña de acceso para la cuenta de administrador"
  )
