from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class Book(BaseModel):
    __tablename__ = "books"
    name = Column(String, nullable=False)
    page_numbers = Column(Integer, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, name={self.name}, author_id={self.author_id})>"
