from pydantic import BaseModel

class ProfileResponse(BaseModel):
  id: int
  first_name: str | None
  last_name: str | None
  role: str
  user_id: int

  class Config:
    from_attributes = True
    use_enum_values = True
