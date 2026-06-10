from fastapi import APIRouter, Depends

from schemas.email import SendEmail
from services.email.email_service import EmailService
from core.security import require_admin

router = APIRouter()


@router.post("/send", dependencies=[Depends(require_admin)])
async def send_email(payload: SendEmail):

    return await EmailService.send_email(
        to=payload.to,
        subject=payload.subject,
        html=payload.html,
    )
