from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from services.rag_engine import rag_engine
from core.security import require_admin

router = APIRouter(prefix="/index", tags=["Indexación"])

@router.post("/start")
async def start_indexing(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    org_id = db.info.get("organization_id")
    return rag_engine.start_indexing_background(org_id=org_id)

@router.get("/status")
async def get_indexing_status(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    org_id = db.info.get("organization_id")
    return await rag_engine.get_indexing_status_complete(org_id=org_id)

@router.post("/reindex")
async def reindex_all(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    org_id = db.info.get("organization_id")
    return await rag_engine.reindex_all_documents(org_id=org_id)
