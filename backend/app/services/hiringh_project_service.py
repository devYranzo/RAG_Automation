import os

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.hiring_project import HiringProject
from models.hiring_project_members import HiringProjectMember
from models.hiring_project_documents import HiringProjectDocument
from models.profile import Profile
from models.user import User

from schemas.hiring_project import (
    HiringProjectCreate,
    HiringProjectUpdate,
    HiringProjectMemberCreate,
    HiringProjectDocumentCreate,
)

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
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")

    if not any(member.user_id == current_user.id for member in project.members):
        raise HTTPException(status_code=403, detail="No tienes acceso a este proyecto.")

    return project


def _get_membership(project: HiringProject, current_user: User) -> HiringProjectMember | None:
    return next((m for m in project.members if m.user_id == current_user.id), None)


def _require_owner(project: HiringProject, current_user: User):
    membership = _get_membership(project, current_user)
    if not membership or membership.role != "OWNER":
        raise HTTPException(
            status_code=403,
            detail="Solo el propietario del proyecto puede realizar esta acción."
        )


def _serialize_project(project: HiringProject, current_user: User) -> dict:
    membership = _get_membership(project, current_user)

    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "search_prompt": project.search_prompt,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "current_user_role": membership.role if membership else None,

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


# ==========================
# LIST / GET
# ==========================

async def get_user_projects(db: AsyncSession, current_user: User):
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
        .join(HiringProjectMember, HiringProjectMember.project_id == HiringProject.id)
        .outerjoin(documents_subquery, documents_subquery.c.project_id == HiringProject.id)
        .outerjoin(members_subquery, members_subquery.c.project_id == HiringProject.id)
        .where(
            HiringProjectMember.user_id == current_user.id,
            HiringProject.organization_id == current_user.organization_id
        )
        .order_by(HiringProject.created_at.desc())
    )

    result = await db.execute(query)
    return result.mappings().all()


async def get_project(db: AsyncSession, current_user: User, project_id: int):
    project = await _get_project_or_403(db, current_user, project_id)
    return _serialize_project(project, current_user)


# ==========================
# CREATE
# ==========================

async def create_project(db: AsyncSession, current_user: User, payload: HiringProjectCreate):
    project = HiringProject(
        organization_id=current_user.organization_id,
        created_by=current_user.id,
        title=payload.title,
        description=payload.description,
        search_prompt=payload.search_prompt,
        status="ACTIVE"
    )
    db.add(project)
    await db.flush()

    owner_membership = HiringProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role="OWNER"
    )
    db.add(owner_membership)

    await db.commit()

    return await get_project(db, current_user, project.id)


# ==========================
# UPDATE
# ==========================

async def update_project(
    db: AsyncSession,
    current_user: User,
    project_id: int,
    payload: HiringProjectUpdate
):
    project = await _get_project_or_403(db, current_user, project_id)
    _require_owner(project, current_user)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.commit()
    return await get_project(db, current_user, project_id)


# ==========================
# DELETE
# ==========================

async def delete_project(db: AsyncSession, current_user: User, project_id: int):
    project = await _get_project_or_403(db, current_user, project_id)
    _require_owner(project, current_user)

    await db.delete(project)
    await db.commit()

    return {"message": "Proyecto eliminado correctamente."}


# ==========================
# MEMBERS
# ==========================

async def add_member(
    db: AsyncSession,
    current_user: User,
    project_id: int,
    payload: HiringProjectMemberCreate
):
    project = await _get_project_or_403(db, current_user, project_id)
    _require_owner(project, current_user)

    result = await db.execute(
        select(User).where(
            User.id == payload.user_id,
            User.organization_id == current_user.organization_id
        )
    )
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en tu organización.")

    if any(m.user_id == target_user.id for m in project.members):
        raise HTTPException(status_code=400, detail="El usuario ya es miembro de este proyecto.")

    # El rol siempre se fuerza a RECRUITER; solo el creador del proyecto es OWNER.
    db.add(HiringProjectMember(
        project_id=project.id,
        user_id=target_user.id,
        role="RECRUITER"
    ))
    await db.commit()

    return await get_project(db, current_user, project_id)


async def remove_member(
    db: AsyncSession,
    current_user: User,
    project_id: int,
    member_id: int
):
    project = await _get_project_or_403(db, current_user, project_id)

    member = next((m for m in project.members if m.id == member_id), None)
    if not member:
        raise HTTPException(status_code=404, detail="Miembro no encontrado.")

    requester = _get_membership(project, current_user)
    is_owner = requester is not None and requester.role == "OWNER"
    is_self = member.user_id == current_user.id

    if not (is_owner or is_self):
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar a este miembro.")

    if member.role == "OWNER":
        owners_count = sum(1 for m in project.members if m.role == "OWNER")
        if owners_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="No puedes eliminar al único propietario del proyecto."
            )

    await db.delete(member)
    await db.commit()

    return await get_project(db, current_user, project_id)


# ==========================
# DOCUMENTS (candidatos añadidos desde el buscador)
# ==========================

async def add_document(
    db: AsyncSession,
    current_user: User,
    project_id: int,
    payload: HiringProjectDocumentCreate
):
    # Basta con ser miembro del proyecto para añadir candidatos, no hace falta ser owner.
    project = await _get_project_or_403(db, current_user, project_id)

    filename = payload.filename or os.path.basename(payload.relative_path)
    folder = os.path.dirname(payload.relative_path) or "General"

    document = HiringProjectDocument(
        project_id=project.id,
        relative_path=payload.relative_path,
        filename=filename,
        folder=folder,
        added_by=current_user.id,
        status="PENDING"
    )
    db.add(document)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Este candidato ya está añadido a este proyecto."
        )

    return await get_project(db, current_user, project_id)