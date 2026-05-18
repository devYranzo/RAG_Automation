from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import event
from sqlalchemy.orm import Session, with_loader_criteria

from fastapi import Request
from jose import jwt

from config import settings
from models.base import HasOrganization

DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://",
    "postgresql+psycopg://"
)

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@event.listens_for(Session, "do_orm_execute")
def _add_organization_filter(execute_state):
    """
    Este interceptor escucha los eventos ORM. Cuando una AsyncSession ejecuta
    un comando, este pasa internamente por los mecanismos de Session y se altera aquí.
    """
    session = execute_state.session

    if session is not None:
        org_id = session.info.get("organization_id")

        # Aplicamos el filtro si hay un ID de organización en la sesión y es un SELECT
        if org_id is not None and execute_state.is_select:
            execute_state.statement = execute_state.statement.options(
                with_loader_criteria(
                    HasOrganization,
                    lambda cls: cls.organization_id == org_id,
                    include_aliases=True,
                    propagate_to_loaders=True
                )
            )

from fastapi import Request
from jose import jwt
from config import settings
# Importa tu SessionLocal asíncrona

async def get_db(request: Request):
    async with SessionLocal() as session:
        try:
            if request:
                token = request.cookies.get("access_token")

                if token and token.lower().startswith("bearer "):
                    token = token.split(" ")[1]

                if token:
                    try:
                        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                        org_id = payload.get("organization_id")

                        if org_id:
                            session.info["organization_id"] = org_id
                    except Exception as jwt_error:
                        print(f"--- Error decodificando la cookie JWT en get_db: {jwt_error} ---")

            yield session

        finally:
            await session.close()
