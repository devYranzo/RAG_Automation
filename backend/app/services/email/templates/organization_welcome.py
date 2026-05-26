from services.email.templates.base_template import base_email_template


def organization_welcome_email(org_name: str, admin_name: str):

    content = f"""
    <h3>Hola {admin_name},</h3>

    <p>Tu organización <b>{org_name}</b> ha sido creada correctamente.</p>

    <p>Desde ahora puedes:</p>
    <ul>
        <li>Crear usuarios</li>
        <li>Subir CVs</li>
        <li>Analizar talento con IA</li>
        <li>Gestionar procesos de selección</li>
    </ul>

    <p>Ya puedes empezar a configurar tu equipo</p>
    """

    return base_email_template(
        content=content,
        cta_url="http://localhost/",
        cta_text="Ir a la app"
    )
