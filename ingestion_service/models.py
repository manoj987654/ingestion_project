from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime

from ingestion_service.database import Base


class ApiRecord(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String, nullable=False)

    external_id = Column(Integer, nullable=False)

    endpoint = Column(String, nullable=False)

    data = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)