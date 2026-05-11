
-- 1. Habilitar la extensión de vectores (requerida por LangChain)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Crear tabla de usuarios para autenticación
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para tabla users
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insert a test user
INSERT INTO users (email, hashed_password, first_name, last_name, is_active)
VALUES (
  'test@email.com',
  '$argon2id$v=19$m=65536,t=3,p=4$PSeEEGIsZUwJgbB2bg2hFA$yEuHZcS4SarZS/8O2lHYlKy4VpaGYQyMiYSpps4P6eQ',
  'Test',
  'Test',
  true
);

-- 3. Crear la tabla que usa LangChain automáticamente
CREATE TABLE IF NOT EXISTS langchain_pg_embedding (
    id VARCHAR PRIMARY KEY,
    collection_id UUID,
    embedding vector(384),
    document TEXT,
    cmetadata JSONB
);

-- 4. Crear tabla auxiliar para las colecciones
CREATE TABLE IF NOT EXISTS langchain_pg_collection (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR,
    cmetadata JSONB
);

-- 5. Crear índices para optimizar las búsquedas
CREATE INDEX IF NOT EXISTS langchain_pg_embedding_embedding_idx
ON langchain_pg_embedding USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS langchain_pg_embedding_collection_id_idx
ON langchain_pg_embedding (collection_id);

CREATE INDEX IF NOT EXISTS langchain_pg_embedding_cmetadata_idx
ON langchain_pg_embedding USING gin (cmetadata);

-- 6. Eliminar la tabla antigua si existe (migración)
DROP TABLE IF EXISTS cv_vectors;
