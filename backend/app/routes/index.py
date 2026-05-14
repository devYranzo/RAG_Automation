from fastapi import APIRouter, Depends
from services.rag_engine import rag_engine
from core.security import require_admin

router = APIRouter(prefix="/index", tags=["Indexación"])

@router.post("/start", dependencies=[Depends(require_admin)])
async def start_indexing():
    return rag_engine.start_indexing_background()

@router.get("/status", dependencies=[Depends(require_admin)])
async def get_indexing_status():
    return await rag_engine.get_indexing_status_complete()

@router.post("/reindex", dependencies=[Depends(require_admin)])
async def reindex_all():
    return await rag_engine.reindex_all_documents()
