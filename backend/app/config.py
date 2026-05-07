import os
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
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 1

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
