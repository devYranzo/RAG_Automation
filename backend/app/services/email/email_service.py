from config import settings
from services.email.resend_client import ResendClient


class EmailService:
    @staticmethod
    async def send_email(to, subject, html):

        payload = {
            "from": settings.EMAIL_FROM,
            "to": [to],
            "subject": subject,
            "html": html,
        }

        return ResendClient.send(payload)
