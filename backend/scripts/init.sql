
-- 1. Habilitar la extensión de vectores (requerida por LangChain)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Crear la tabla que usa LangChain automáticamente
CREATE TABLE IF NOT EXISTS langchain_pg_embedding (
    id VARCHAR PRIMARY KEY,
    collection_id UUID,
    embedding vector(384),
    document TEXT,
    cmetadata JSONB
);

-- 3. Crear tabla auxiliar para las colecciones
CREATE TABLE IF NOT EXISTS langchain_pg_collection (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR,
    cmetadata JSONB
);

-- 4. Crear índices para optimizar las búsquedas
CREATE INDEX IF NOT EXISTS langchain_pg_embedding_embedding_idx
ON langchain_pg_embedding USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS langchain_pg_embedding_collection_id_idx
ON langchain_pg_embedding (collection_id);

CREATE INDEX IF NOT EXISTS langchain_pg_embedding_cmetadata_idx
ON langchain_pg_embedding USING gin (cmetadata);

-- 5. Eliminar la tabla antigua si existe (migración)
DROP TABLE IF EXISTS cv_vectors;
