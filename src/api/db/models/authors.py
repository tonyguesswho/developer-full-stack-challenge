from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship

from .base import BaseModel


class Author(BaseModel):
    __tablename__ = "authors"

    name = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"
