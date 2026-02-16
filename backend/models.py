from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from db import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String, index=True)
    storage_path = Column(String)
    status = Column(String, default="CREATED", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
