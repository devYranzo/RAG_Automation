from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from services.rag_engine import rag_engine
from core.security import require_any_user, require_admin

router = APIRouter(tags=["Buscador"])

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_rag(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_any_user)
):
    org_id = db.info.get("organization_id")

    return await rag_engine.query(question=request.question, org_id=org_id)

@router.post("/cache/clear")
async def clear_cache(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    rag_engine.clear_cache()
    return {"status": "cache_cleared"}
