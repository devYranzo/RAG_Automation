from pydantic import BaseModel, EmailStr

class SendEmail(BaseModel):
    to: EmailStr
    subject: str
    html: str
