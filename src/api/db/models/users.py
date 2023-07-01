from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(), unique=True)
    password = Column(String())

    jwt = relationship(
        "Jwt", foreign_keys="Jwt.user_id", back_populates="user", lazy=True
    )

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Jwt(BaseModel):
    __tablename__ = "jwts"
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user = relationship("User", foreign_keys=[user_id], back_populates="jwt")
    access = Column(String())
    refresh = Column(String())

    def __repr__(self):
        return f"Access - {self.access} | Refresh - {self.refresh}"
