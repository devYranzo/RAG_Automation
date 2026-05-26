import resend
from config import settings

resend.api_key = settings.RESEND_API_KEY

class ResendClient:

    @staticmethod
    def send(params):
        return resend.Emails.send(params)
