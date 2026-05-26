from services.company.company_service import create_company
from services.email.email_service import EmailService
from services.email.templates.organization_welcome import organization_welcome_email


async def register_company_flow(db, payload):

    result = await create_company(db, payload)

    org = result["organization"]
    user = result["user"]
    profile = result["profile"]

    # EMAIL
    html = organization_welcome_email(
        org_name=org.name,
        admin_name=profile.first_name
    )

    await EmailService.send_email(
        to=user.email,
        subject=f"Bienvenido a Talent Finder",
        html=html
    )

    return result
