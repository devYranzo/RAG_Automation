from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from models.base import Base

class AnalyticsQuery(Base):
    __tablename__ = "analytics_queries"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(String, index=True, nullable=False)
    usuario_id = Column(Integer, nullable=True)
    usuario_nombre = Column(String, nullable=True)

    query = Column(String, nullable=False)
    skills_detectadas = Column(JSON, nullable=False)
    cached = Column(Boolean, default=False)
    resultados_count = Column(Integer, default=0)
    latencia = Column(Float, nullable=True, default=0.0)
    
    tokens_input = Column(Integer, nullable=True, default=0)
    tokens_output = Column(Integer, nullable=True, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
