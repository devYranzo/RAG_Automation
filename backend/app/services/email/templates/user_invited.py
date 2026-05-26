from services.email.templates.base_template import base_email_template


def user_invited_email(user_name: str, org_name: str):

    content = f"""
    <h3>Hola {user_name},</h3>

    <p>Has sido añadido a la organización <b>{org_name}</b>.</p>

    <p>Ahora puedes acceder a la plataforma para:</p>
    <ul>
        <li>Ver análisis de CVs</li>
        <li>Consultar candidatos</li>
        <li>Participar en procesos de selección</li>
    </ul>

    <p>Tu equipo ya te está esperando 👋</p>
    """

    return base_email_template(
        content=content,
        cta_url="http://localhost/",
        cta_text="Acceder ahora"
    )
