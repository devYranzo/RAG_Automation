from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from services.rag_engine import rag_engine
from core.security import require_any_user

router = APIRouter(prefix="/system", tags=["Sistema"])

@router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_any_user)
):
    """Estadísticas del motor RAG filtradas por la organización del usuario actual"""

    org_id = db.info.get("organization_id")

    vector_count = await rag_engine.get_vector_count(org_id=org_id)
    document_count = await rag_engine.get_indexed_documents_count(org_id=org_id)
    is_indexed = await rag_engine.is_indexed(org_id=org_id)
    indexing_status = rag_engine.get_indexing_status()
    total_pdfs = rag_engine.get_total_pdf_files(org_id=org_id)

    return {
        "is_indexed": is_indexed,
        "vectors_count": vector_count,
        "documents_count": document_count,
        "total_pdfs": total_pdfs,

        "indexing": indexing_status,
        "cache_size": len(rag_engine._query_cache)
    }
