import os
from pathlib import Path


def organization_welcome_email(org_name: str, admin_name: str, cta_url: str = "http://localhost"):
    """
    Load and render the organization welcome email template from HTML.

    Args:
        org_name: Name of the organization
        admin_name: Name of the admin user
        cta_url: Call-to-action URL (dashboard link)

    Returns:
        Rendered HTML email template with variables replaced
    """
    # Get the path to the HTML template
    template_dir = Path(__file__).parent
    template_path = template_dir / "organization_welcome.html"

    # Read the HTML template
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("{{ORG_NAME}}", org_name)
    html_content = html_content.replace("{{ADMIN_NAME}}", admin_name)
    html_content = html_content.replace("{{CTA_URL}}", cta_url)

    return html_content
