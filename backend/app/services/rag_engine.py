import time
import asyncio
import os
import json
import traceback
from datetime import datetime, timezone
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy import text, create_engine, bindparam, JSON

from config import settings
from database import get_vector_store
from database import engine as db_engine


class RAGEngine:
    def __init__(self):
        self.vector_store = get_vector_store()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0,
            max_retries=3,
            timeout=120,
            request_timeout=120
        )

        # INGESTION STATE
        self.is_indexing = False
        self.processed_documents = 0
        self.total_documents = 0
        self.indexing_error: Optional[str] = None

        # CACHE
        self._query_cache = {}
        self._cache_ttl = 300
        self._retriever = None

        self._sync_engine = None
        self._indexing_task: Optional[asyncio.Task] = None

    # =========================================================
    # DB ENGINE
    # =========================================================
    def _get_sync_engine(self):
        if self._sync_engine is None:
            db_url = settings.DATABASE_URL.replace('+asyncpg', '')
            self._sync_engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_recycle=3600
            )
        return self._sync_engine

    # =========================================================
    # INDEXING CORE (Aislado por Organización)
    # =========================================================
    def _index_documents_sync(self, org_id: int):
        self.indexing_error = None

        try:
            tenant_pdf_path = os.path.join(settings.PDF_PATH, f"org_{org_id}")
            if not os.path.exists(tenant_pdf_path):
                os.makedirs(tenant_pdf_path, exist_ok=True)

            loader = DirectoryLoader(
                tenant_pdf_path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader,
                recursive=True
            )
            docs = loader.load()

            existing_ids = set()
            try:
                sync_engine = self._get_sync_engine()
                with sync_engine.connect() as conn:
                    collection_result = conn.execute(
                        text("SELECT uuid FROM langchain_pg_collection WHERE name = :name LIMIT 1"),
                        {"name": settings.COLLECTION_NAME}
                    )
                    collection_uuid = collection_result.scalar()

                    if collection_uuid:
                        result = conn.execute(
                            text("""
                                SELECT DISTINCT cmetadata->>'source'
                                FROM langchain_pg_embedding
                                WHERE collection_id = :uuid
                                AND cmetadata->>'organization_id' = :org_id
                            """),
                            {"uuid": collection_uuid, "org_id": str(org_id)}
                        )
                        existing_ids = {row[0] for row in result}

            except Exception as e:
                print(f"[WARN] existing docs: {e}")

            new_docs = [
                d for d in docs
                if d.metadata.get('source') not in existing_ids
            ]

            if not new_docs:
                self.total_documents = len(docs)
                self.processed_documents = 0
                return 0

            self.total_documents = len(new_docs)
            self.processed_documents = 0

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150
            )
            chunks = splitter.split_documents(new_docs)

            for c in chunks:
                c.page_content = c.page_content.replace("\x00", "")
                c.metadata["organization_id"] = str(org_id)

            batch_size = 20
            batches = [
                chunks[i:i + batch_size]
                for i in range(0, len(chunks), batch_size)
            ]

            total_batches = len(batches)

            for i, batch in enumerate(batches):
                if not self.is_indexing:
                    break

                try:
                    self.vector_store.add_documents(batch)

                    self.processed_documents = min(
                        self.total_documents,
                        int((i + 1) / total_batches * self.total_documents)
                    )

                    time.sleep(1.5 if i < 10 else 2.5)

                except Exception as e:
                    print(f"[ERROR batch]: {e}")
                    time.sleep(5)

            self._query_cache.clear()
            self._retriever = None

            return len(chunks)

        except Exception as e:
            self.indexing_error = str(e)
            return 0

        finally:
            self.is_indexing = False

    # =========================================================
    # ASYNC INDEXING
    # =========================================================
    async def index_documents_async(self, org_id: int):
        if self.is_indexing:
            return {"status": "already_running"}

        self.is_indexing = True

        try:
            result = await asyncio.to_thread(self._index_documents_sync, org_id)
            return {"status": "completed", "chunks": result}
        finally:
            self.is_indexing = False

    def start_indexing_background(self, org_id: int):
        if self._indexing_task and not self._indexing_task.done():
            return {"status": "already_running"}

        loop = asyncio.get_event_loop()
        self._indexing_task = loop.create_task(self.index_documents_async(org_id))

        return {"status": "started"}

    # ==========================================
    # REINDEX
    # ==========================================
    async def reindex_all_documents(self, org_id: int):
        try:
            sync_engine = self._get_sync_engine()
            with sync_engine.connect() as conn:
                conn.execute(
                    text("DELETE FROM langchain_pg_embedding WHERE cmetadata->>'organization_id' = :org_id"),
                    {"org_id": str(org_id)}
                )
                conn.commit()

            return self.start_indexing_background(org_id)

        except Exception as e:
            return {"status": "error", "message": str(e)}

    # =========================================================
    # QUERY
    # =========================================================
    async def query(self, question: str, org_id: int, usuario_id: str = "1", usuario_nombre: str = "Usuario Sistema"):
        start_time = time.time()
        cache_key = f"org_{org_id}_" + question.lower().strip()
        now = time.time()

        if cache_key in self._query_cache:
            res, ts = self._query_cache[cache_key]
            if now - ts < self._cache_ttl:
                latencia_cache = time.time() - start_time
                await self._registrar_metrica_en_bd(
                    org_id=org_id, usuario_id=usuario_id, usuario_nombre=usuario_nombre,
                    query=question, cached=True, latencia=latencia_cache,
                    resultados_count=len(res.get("sources", [])), tokens_input=0, tokens_output=0,
                    skills=["Caché Hit"]
                )
                return res

        self._retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 10,
                "filter": {"organization_id": str(org_id)}
            }
        )

        try:
            docs = await asyncio.wait_for(
                asyncio.to_thread(self._retriever.invoke, question),
                timeout=8.0
            )
        except asyncio.TimeoutError:
            return {"answer": "Timeout en búsqueda.", "sources": []}

        docs_by_source = {}
        for d in docs:
            src = d.metadata.get("source", "unknown")
            relative_src = os.path.relpath(src, settings.PDF_PATH) if src != "unknown" else src

            docs_by_source.setdefault(relative_src, [])
            if len(docs_by_source[relative_src]) < 2:
                docs_by_source[relative_src].append(d.page_content)

        context = "\n\n---\n\n".join(
            f"ARCHIVO: {k}\n{''.join(v)[:800]}"
            for k, v in docs_by_source.items()
        )

        prompt = ChatPromptTemplate.from_template(
            """Eres un motor de selección de personal. Retorna exactamente los 5 mejores candidatos.

            INSTRUCCIONES:
            1. Solo los 5 mejores candidatos
            2. Formato estricto por candidato

            FORMATO POR CANDIDATO:
            ### Nombre Completo
            [BOTON_CV:{{filename}}] **Por qué encaja:** [Razón técnica y cultural]
            **Experiencia:** [Años] años | [Cargo actual] | [Idiomas]
            **Skills:** [Tecnologías clave]
            **Educación:** [Titulación más alta]

            ---

            DATOS:
            {context}

            SOLICITUD:
            {question}

            IMPORTANTE: En {{filename}} pon la ruta exacta que aparece en "ARCHIVO".
            """
        )

        chain = prompt | self.llm
        response = await chain.ainvoke({"context": context, "question": question})
        answer = str(response.content)

        # ─── EXTRACCIÓN BLINDADA DE TOKENS (Múltiples variantes de LangChain) ───
        t_input = 0
        t_output = 0

        # Estrategia A: response.response_metadata estándar
        meta = getattr(response, "response_metadata", {}) or {}
        usage = meta.get("token_usage", {}) or {}

        # Estrategia B: Por si viene directo como claves en response_metadata
        if not usage:
            usage = meta

        t_input = usage.get("prompt_tokens") or usage.get("input_tokens") or usage.get("usage", {}).get("prompt_tokens", 0)
        t_output = usage.get("completion_tokens") or usage.get("output_tokens") or usage.get("usage", {}).get("completion_tokens", 0)

        # Estrategia C: Introspección cruda de generación si todo lo anterior es 0
        if t_input == 0 and hasattr(response, "usage_metadata"):
            usage_meta = getattr(response, "usage_metadata", {}) or {}
            t_input = usage_meta.get("input_tokens", 0)
            t_output = usage_meta.get("output_tokens", 0)

        result = {
            "answer": answer,
            "sources": list(docs_by_source.keys())
        }

        self._query_cache[cache_key] = (result, now)

        skills_encontradas = ["RAG"]
        keywords_skills = ["python", "javascript", "vue", "react", "sql", "aws", "docker", "node", "java", "php"]
        for kw in keywords_skills:
            if kw in question.lower() or kw in context.lower():
                skills_encontradas.append(kw.upper())

        latencia_total = time.time() - start_time

        await self._registrar_metrica_en_bd(
            org_id=org_id, usuario_id=usuario_id, usuario_nombre=usuario_nombre,
            query=question, cached=False, latencia=latencia_total,
            resultados_count=len(result["sources"]), tokens_input=t_input, tokens_output=t_output,
            skills=list(set(skills_encontradas))
        )

        return result

    async def _registrar_metrica_en_bd(self, org_id, usuario_id, usuario_nombre, query, cached, latencia, resultados_count, tokens_input, tokens_output, skills):
        try:
            org_id_seguro = str(org_id)
            try:
                usuario_id_seguro = int(usuario_id) if usuario_id is not None else None
            except (ValueError, TypeError):
                usuario_id_seguro = None

            skills_seguras = skills if (skills and isinstance(skills, list)) else ["RAG"]

            stmt = text("""
                INSERT INTO analytics_queries
                (organization_id, usuario_id, usuario_nombre, query, cached, latencia, resultados_count, tokens_input, tokens_output, skills_detectadas, created_at)
                VALUES (:org_id, :usuario_id, :usuario_nombre, :query, :cached, :latencia, :resultados_count, :t_input, :t_output, :skills, :created_at)
            """).bindparams(bindparam("skills", type_=JSON))

            async with db_engine.begin() as conn:
                await conn.execute(
                    stmt,
                    {
                        "org_id": org_id_seguro,
                        "usuario_id": usuario_id_seguro,
                        "usuario_nombre": str(usuario_nombre) if usuario_nombre else "Usuario Sistema",
                        "query": str(query)[:255],
                        "cached": bool(cached),
                        "latencia": float(latencia) if latencia is not None else 0.0,
                        "resultados_count": int(resultados_count) if resultados_count is not None else 0,
                        "t_input": int(tokens_input),
                        "t_output": int(tokens_output),
                        "skills": skills_seguras,
                        "created_at": datetime.now(timezone.utc).replace(tzinfo=None)
                    }
                )
            print(f"[SUCCESS] Métrica guardada. Tokens In: {tokens_input} | Out: {tokens_output}")
        except Exception as e:
            print("\n[ERROR CRÍTICO AL GUARDAR EN ANALYTICS_QUERIES]:")
            traceback.print_exc()

    # =========================================================
    # STATS
    # =========================================================
    async def get_vector_count(self, org_id: int):
        try:
            async with db_engine.connect() as conn:
                res = await conn.execute(
                    text("SELECT count(*) FROM langchain_pg_embedding WHERE cmetadata->>'organization_id' = :org_id"),
                    {"org_id": str(org_id)}
                )
                return res.scalar() or 0
        except:
            return 0

    def get_total_pdf_files(self, org_id: int):
        total = 0
        tenant_pdf_path = os.path.join(settings.PDF_PATH, f"org_{org_id}")
        if not os.path.exists(tenant_pdf_path):
            return 0
        for root, dirs, files in os.walk(tenant_pdf_path):
            total += len([file for file in files if file.lower().endswith(".pdf")])
        return total

    async def get_indexed_documents_count(self, org_id: int):
        try:
            async with db_engine.connect() as conn:
                res = await conn.execute(text("""
                    SELECT count(DISTINCT cmetadata->>'source')
                    FROM langchain_pg_embedding
                    WHERE cmetadata->>'organization_id' = :org_id
                """), {"org_id": str(org_id)})
                return res.scalar() or 0
        except:
            return 0

    def get_indexing_status(self):
        total = self.total_documents or 0
        processed = self.processed_documents or 0
        return {
            "is_indexing": self.is_indexing,
            "processed": processed,
            "total": total,
            "progress_percent": int((processed / total) * 100) if total > 0 else 0,
            "error": self.indexing_error
        }

    async def get_indexing_status_complete(self, org_id: int):
        v_count = await self.get_vector_count(org_id)
        d_count = await self.get_indexed_documents_count(org_id)
        total_pdfs = self.get_total_pdf_files(org_id)
        return {
            **self.get_indexing_status(),
            "has_data": v_count > 0,
            "vectors_count": v_count,
            "documents_count": d_count,
            "total_pdfs": total_pdfs
        }

    async def is_indexed(self, org_id: int):
        return (await self.get_vector_count(org_id)) > 0

    def clear_cache(self):
        self._query_cache.clear()
        self._retriever = None
        return {"status": "cache_cleared"}


rag_engine = RAGEngine()
