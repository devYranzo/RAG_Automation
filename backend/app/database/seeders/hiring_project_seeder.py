from sqlalchemy import select

from models.hiring_project import HiringProject
from models.hiring_project_members import HiringProjectMember
from models.hiring_project_documents import HiringProjectDocument


async def seed_hiring_projects(session):

    stmt = select(HiringProject).where(HiringProject.id == 1)
    result = await session.execute(stmt)

    existing_project = result.scalar_one_or_none()

    if existing_project:
        return

    # ==========================
    # Proyecto
    # ==========================

    project = HiringProject(
        id=1,
        organization_id=1,
        created_by=1,
        title="Backend Python Senior",
        description="Proceso de selección de ejemplo.",
        search_prompt="Python FastAPI PostgreSQL Docker AWS",
        status="ACTIVE"
    )

    session.add(project)

    await session.flush()

    # ==========================
    # Miembro
    # ==========================

    member = HiringProjectMember(
        project_id=project.id,
        user_id=1,
        role="OWNER"
    )

    session.add(member)

    # ==========================
    # Documento
    # ==========================

    document = HiringProjectDocument(
        project_id=project.id,
        relative_path="org_1/Prueba/cv-eneko-yranzo-redondo-1.pdf",
        filename="cv-eneko-yranzo-redondo.pdf",
        folder="Prueba",
        added_by=1,
        status="PENDING"
    )

    session.add(document)

    await session.flush()