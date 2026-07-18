from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.hiring_project import HiringProject
from models.hiring_project_members import HiringProjectMember
from models.hiring_project_documents import HiringProjectDocument
from models.profile import Profile
from models.user import User

# PRIVATE
async def _get_project_or_403(
    db: AsyncSession,
    current_user: User,
    project_id: int
) -> HiringProject:

    query = (
        select(HiringProject)
        .where(
            HiringProject.id == project_id,
            HiringProject.organization_id == current_user.organization_id
        )
        .options(
            selectinload(HiringProject.members)
            .selectinload(HiringProjectMember.user)
            .selectinload(User.profile),

            selectinload(HiringProject.documents)
        )
    )

    result = await db.execute(query)

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado."
        )

    if not any(member.user_id == current_user.id for member in project.members):
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a este proyecto."
        )

    return project


# GET PROJECTS
async def get_user_projects(
    db: AsyncSession,
    current_user: User
):

    documents_subquery = (
        select(
            HiringProjectDocument.project_id,
            func.count(HiringProjectDocument.id).label("documents_count")
        )
        .group_by(HiringProjectDocument.project_id)
        .subquery()
    )

    members_subquery = (
        select(
            HiringProjectMember.project_id,
            func.count(HiringProjectMember.id).label("members_count")
        )
        .group_by(HiringProjectMember.project_id)
        .subquery()
    )

    query = (
        select(
            HiringProject.id,
            HiringProject.title,
            HiringProject.description,
            HiringProject.status,
            HiringProject.created_at,
            HiringProject.updated_at,
            func.coalesce(documents_subquery.c.documents_count, 0).label("documents_count"),
            func.coalesce(members_subquery.c.members_count, 0).label("members_count"),
        )
        .join(
            HiringProjectMember,
            HiringProjectMember.project_id == HiringProject.id
        )
        .outerjoin(
            documents_subquery,
            documents_subquery.c.project_id == HiringProject.id
        )
        .outerjoin(
            members_subquery,
            members_subquery.c.project_id == HiringProject.id
        )
        .where(
            HiringProjectMember.user_id == current_user.id,
            HiringProject.organization_id == current_user.organization_id
        )
        .order_by(HiringProject.created_at.desc())
    )

    result = await db.execute(query)

    projects = result.mappings().all()

    return projects

# GET PROJECT
async def get_project(
    db: AsyncSession,
    current_user: User,
    project_id: int
):

    project = await _get_project_or_403(
        db=db,
        current_user=current_user,
        project_id=project_id
    )

    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "search_prompt": project.search_prompt,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,

        "members": [
            {
                "id": member.id,
                "user_id": member.user.id,
                "username": (
                    f"{member.user.profile.first_name} {member.user.profile.last_name}"
                    if member.user.profile
                    else member.user.email
                ),
                "email": member.user.email,
                "role": member.role
            }
            for member in project.members
        ],

        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "relative_path": doc.relative_path,
                "status": doc.status,
                "added_by": doc.added_by,
                "created_at": doc.created_at
            }
            for doc in project.documents
        ]
    }