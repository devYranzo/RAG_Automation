from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from schemas.hiring_project import HiringProjectListResponse, HiringProjectDetailResponse

from services.hiringh_project_service import get_user_projects, get_project
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


@router.get('/{project_id}', response_model=HiringProjectDetailResponse, dependencies=[Depends(require_recruiter)])
async def get_user_project(
        project_id: int, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await get_project(db, current_user, project_id)
