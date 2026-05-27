from services.company.company_service import create_company, delete_company
from services.email.email_service import EmailService
from services.email.templates.organization_welcome import organization_welcome_email
from services.file_manager import file_manager


async def register_company_flow(db, payload):
    result = await create_company(db, payload)

    org = result["organization"]
    user = result["user"]
    profile = result["profile"]

    file_manager.create_org_storage(org.id)

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

async def delete_company_flow(db, org_id: int):
    result = await delete_company(db, org_id)

    if not result:
        return {"message": "Organization not found"}

    file_manager.delete_org_storage(org_id)

    return {
        "message": f"Organization {org_id} deleted successfully"
    }
