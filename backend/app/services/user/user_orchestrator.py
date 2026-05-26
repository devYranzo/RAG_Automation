from services.user.user_service import create_user_with_profile
from services.email.email_service import EmailService
from services.email.templates.user_invited import user_invited_email


async def create_user_flow(db, user_in):

    user = await create_user_with_profile(db, user_in)

    html = user_invited_email(
        user_name=user.profile.first_name,
        org_name=user.organization.name
    )

    await EmailService.send_email(
        to=user.email,
        subject="Bienvenido",
        html=html
    )

    return user
