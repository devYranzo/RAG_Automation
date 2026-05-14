from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.rag_engine import rag_engine
from core.security import require_any_user

router = APIRouter(tags=["Buscador"])

class QueryRequest(BaseModel):
    question: str

@router.post("/query", dependencies=[Depends(require_any_user)])
async def query_rag(request: QueryRequest):
    return await rag_engine.query(request.question)

@router.post("/cache/clear")
async def clear_cache():
    rag_engine.clear_cache()
    return {"status": "cache_cleared"}
