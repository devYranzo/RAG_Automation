from pydantic import BaseModel

class ProfileResponse(BaseModel):
  profile_id: int
  first_name: str | None
  last_name: str | None
  role: str
  email: str
  is_active: bool


  class Config:
    from_attributes = True
    use_enum_values = True
