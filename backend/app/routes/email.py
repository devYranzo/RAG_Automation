from fastapi import APIRouter

from schemas.email import SendEmail
from services.email.email_service import EmailService

router = APIRouter()


@router.post("/send")
async def send_email(payload: SendEmail):

    return await EmailService.send_email(
        to=payload.to,
        subject=payload.subject,
        html=payload.html,
    )
