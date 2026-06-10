# TalentFinder: Análisis Inteligente de CVs

**TalentFinder** es una solución avanzada de reclutamiento basada en **RAG (Retrieval-Augmented Generation)**. Permite a los departamentos de RRHH indexar cientos de currículos en PDF y realizar consultas complejas en lenguaje natural para identificar a los candidatos ideales basándose en su experiencia, formación y certificaciones.

---

## 🛠️ Stack Tecnológico

- **Frontend:** Vue.js 3 (Composition API), Vite, Bootstrap 5.
- **Backend:** FastAPI (Python 3.11+), LangChain, SQLAlchemy.
- **Base de Datos Vectorial:** PostgreSQL + **PGVector**.
- **Embeddings:** intfloat/multilingual-e5-small (HuggingFace).
- **LLM:** Google Gemini 2.5 Flash Lite.
- **Infraestructura:** Docker & Docker Compose.

---

## ✨ Características Destacadas

- **🔍 Búsqueda Semántica:** Entiende conceptos técnicos y contextos, no solo palabras clave.
- **📊 Monitorización en Tiempo Real:** Barra de progreso reactiva que muestra el estado de la indexación.
- **📁 Gestor de Archivos Integrado:** Carga de PDFs organizados en carpetas con vista en tiempo real.
- **📋 Ranking Inteligente:** Los 5 mejores candidatos ordenados por relevancia.
- **🐳 Dockerizado:** Despliegue sencillo con un solo comando.

---

## 🏗️ Arquitectura del Sistema

El flujo de trabajo sigue el estándar RAG para garantizar respuestas precisas:

1. **Indexación:** Los archivos PDF se cargan mediante el File Manager y se almacenan en `/storage/CVs`.
2. **Fragmentación:** `RecursiveCharacterTextSplitter` (1500 chars, 150 overlap) mantiene contexto en cada fragmento.
3. **Embeddings & Storage:** Vectores generados con intfloat/multilingual-e5-small y almacenados en PGVector.
4. **Búsqueda:** Similarity search (optimizado, ~6-8 segundos) para recuperar los CVs más relevantes.
5. **Ranking:** LLM genera ranking de 5 mejores candidatos con análisis detallado.
6. **Caching:** Sistema de caché para consultas repetidas (TTL: 5 minutos).

---

## 🚀 Instalación y Despliegue

### Requisitos Previos

- Docker y Docker Compose instalados.
- API Key de Google Gemini válida.

### Pasos para arrancar

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/devYranzo/RAG_Automation.git
   cd talentfinder-rag
   ```

2. **Configurar el entorno:**
   Crea un archivo `.env` en `backend/`:

   ```env
   # AI Model
   GOOGLE_API_KEY=tu_api_key_aquí

   # Database Configuration
   DATABASE_URL=postgresql+psycopg://user:password@db:5432/rag_db

   # Authentication
   SECRET_KEY = "secret-key-change-this"

   # Mail Service
   RESEND_API_KEY=tu_api_key_aquí
   ```

3. **Desplegar:**

   ```bash
   docker compose build
   ```

   ```bash
   docker compose up -d
   ```

4. **Acceso:**
   - **Frontend:** `http://localhost`
   - **API (Swagger):** `http://localhost:8000/docs`
   - **Backend API:** `http://localhost:8000`

---

## 📂 Estructura del Proyecto

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app principal
│   │   ├── config.py            # Configuración (env vars)
│   │   ├── database.py          # Conexión BD y vectorstore
│   │   ├── engine.py            # Motor RAG principal
│   │   ├── routes/              # Endpoints organizados
│   │   │   ├── index.py         # POST /index/start, GET /index/status
│   │   │   ├── search.py        # POST /query
│   │   │   ├── file_manager.py  # Gestión de PDFs
│   │   │   ├── system.py        # GET /system/stats
│   │   │   └── admin.py         # Endpoints admin
│   │   └── services/
│   │       └── file_manager.py  # Lógica de almacenamiento
│   ├── storage/
│   │   └── CVs/                 # Almacenamiento persistente de PDFs
│   ├── scripts/
│   │   └── init.sql             # Script inicialización BD
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── assets/
│   │   │   └── style.css
│   │   ├── components/
│   │   │   ├── Header.vue
│   │   │   ├── SearchBar.vue
│   │   │   ├── ResultCard.vue
│   │   │   └── IngestProgress.vue
│   │   ├── views/
│   │   │   ├── HomeView.vue     # Vista principal
│   │   │   └── FileManager.vue  # Gestor de archivos
│   │   ├── composables/
│   │   │   ├── useSearch.js     # Lógica de búsqueda
│   │   │   ├── useMotorStatus.js # Estado de indexación
│   │   │   └── useTheme.js      # Tema (dark/light)
│   │   ├── services/
│   │   │   └── api.js           # Cliente HTTP (axios)
│   │   └── router/
│   │       └── index.js         # Rutas de la app
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

---

## 🔌 Endpoints Principales

### Indexación

- `POST /index/start` - Inicia la indexación de PDFs en background
- `GET /index/status` - Obtiene estado actual de indexación
- `POST /index/reindex` - Elimina todo e indexa de nuevo

### Búsqueda

- `POST /query` - Realiza búsqueda semántica (body: `{"question": "..."}`)

### File Manager

- `POST /filemanager/upload` - Sube un PDF a una carpeta
- `GET /filemanager/folders` - Lista carpetas disponibles
- `GET /filemanager/list` - Lista árbol de archivos
- `POST /filemanager/create-folder` - Crea nueva carpeta

### Sistema

- `GET /system/stats` - Estadísticas globales (documentos, vectores, etc.)

---

## 🤝 Autor

Proyecto desarrollado por devYranzo - 2026.
