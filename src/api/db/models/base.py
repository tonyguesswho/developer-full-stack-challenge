import uuid
from datetime import datetime

from core.database import Base
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(Base):
    __abstract__ = True
    pkid = Column(Integer, primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
