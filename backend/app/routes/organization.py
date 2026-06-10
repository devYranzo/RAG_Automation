from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db

from services.company.company_orchestrator import delete_company_flow
from core.security import require_admin

router = APIRouter(prefix="/organization", tags=["Organization"])

@router.delete("/delete/{org_id}")
async def delete_organization(
    org_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    return await delete_company_flow(db, org_id)
