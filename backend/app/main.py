from contextlib import asynccontextmanager
from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import auth, index, search, system, file_manager, profile, users, analytics, email, organization, hiring_projects
from database.db import engine
from database.seeders import run_seeders

from models.user import User
from models.profile import Profile
from models.analytics import AnalyticsQuery
from models.organization import Organization
from models.hiring_project import HiringProject
from models.hiring_project_members import HiringProjectMember
from models.hiring_project_documents import HiringProjectDocument
from models.hiring_project_notes import HiringProjectNote
from models.base import Base

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await run_seeders()
    yield

app = FastAPI(
    title="TalentFinder API",
    lifespan=lifespan
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def validate_csrf_origin(request: Request, call_next):
    unsafe_method = request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}
    uses_cookie_auth = "access_token" in request.cookies

    if unsafe_method and uses_cookie_auth:
        origin = request.headers.get("origin")
        referer = request.headers.get("referer")
        source = origin or referer

        if not source:
            return JSONResponse(
                status_code=403,
                content={"detail": "Origen de la petición no verificable."}
            )

        parsed = urlparse(source)
        request_origin = f"{parsed.scheme}://{parsed.netloc}"

        if request_origin not in settings.ALLOWED_ORIGINS:
            return JSONResponse(
                status_code=403,
                content={"detail": "Origen de la petición no permitido."}
            )

    return await call_next(request)

# Routes
app.include_router(auth.router)

app.include_router(index.router)
app.include_router(search.router)
app.include_router(system.router)

app.include_router(file_manager.router)
app.include_router(file_manager.pdfs_router)

app.include_router(organization.router)
app.include_router(profile.router)
app.include_router(users.router)

app.include_router(analytics.router)

app.include_router(hiring_projects.router)

app.include_router(email.router)
