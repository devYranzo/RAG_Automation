import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """ Database configuration """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    COLLECTION_NAME: str = "cv_vectors"

    """ AI Models """
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-small"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    """ CVs directory """
    PDF_PATH: str = "/storage/CVs"

    """ Authentication """
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 4

    """ Mail Service """
    EMAIL_FROM: str = "noreply@mail.enekoyranzo.dev"
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")

    class Config:
        env_file = (".env", "../.env")
        extra = "ignore"

settings = Settings()
