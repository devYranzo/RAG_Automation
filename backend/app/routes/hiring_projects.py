from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from schemas.hiring_project import (
    HiringProjectListResponse,
    HiringProjectDetailResponse,
    HiringProjectCreate,
    HiringProjectUpdate,
    HiringProjectMemberCreate,
    HiringProjectDocumentCreate,
)

from services.hiringh_project_service import (
    get_user_projects,
    get_project,
    create_project,
    update_project,
    delete_project,
    add_member,
    remove_member,
    add_document,
)
from core.security import get_current_user, require_recruiter
from models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/list",
    response_model=list[HiringProjectListResponse],
    dependencies=[Depends(require_recruiter)]
)
async def get_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_user_projects(db, current_user)


@router.post(
    "/create",
    response_model=HiringProjectDetailResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_recruiter)]
)
async def create_new_project(
    payload: HiringProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_project(db, current_user, payload)


@router.get(
    '/{project_id}',
    response_model=HiringProjectDetailResponse,
    dependencies=[Depends(require_recruiter)]
)
async def get_user_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_project(db, current_user, project_id)


@router.patch(
    '/{project_id}',
    response_model=HiringProjectDetailResponse,
    dependencies=[Depends(require_recruiter)]
)
async def update_existing_project(
    project_id: int,
    payload: HiringProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_project(db, current_user, project_id, payload)


@router.delete(
    '/{project_id}',
    dependencies=[Depends(require_recruiter)]
)
async def delete_existing_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_project(db, current_user, project_id)


@router.post(
    '/{project_id}/members',
    response_model=HiringProjectDetailResponse,
    dependencies=[Depends(require_recruiter)]
)
async def add_project_member(
    project_id: int,
    payload: HiringProjectMemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await add_member(db, current_user, project_id, payload)


@router.delete(
    '/{project_id}/members/{member_id}',
    response_model=HiringProjectDetailResponse,
    dependencies=[Depends(require_recruiter)]
)
async def remove_project_member(
    project_id: int,
    member_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await remove_member(db, current_user, project_id, member_id)


@router.post(
    '/{project_id}/documents',
    response_model=HiringProjectDetailResponse,
    dependencies=[Depends(require_recruiter)]
)
async def add_project_document(
    project_id: int,
    payload: HiringProjectDocumentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await add_document(db, current_user, project_id, payload)