import uuid
from typing import List, Optional

from pydantic import BaseModel, Field


class AuthorBookResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    page_numbers: int
    # author: AuthorResponseSchema

    class Config:
        orm_mode = True


class AuthorResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    book_count: int = 0
    books: List[AuthorBookResponseSchema]

    class Config:
        orm_mode = True


class AuthorUpdateSchema(BaseModel):
    name: str


class BookResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    page_numbers: int
    author: AuthorResponseSchema

    class Config:
        orm_mode = True


class BookCreateSchema(BaseModel):
    name: str
    page_numbers: int = Field(0, alias="pages")
    author_id: uuid.UUID = Field("", alias="author")


class BookCreateWithAuthorSchema(BaseModel):
    name: str
    page_numbers: int = Field(0, alias="pages")


class AuthorCreateSchema(BaseModel):
    name: str
    books: Optional[List[BookCreateWithAuthorSchema]] = []


class BookUpdate(BaseModel):
    id: uuid.UUID
    name: str
    page_numbers: int


class AuthorUpdateSchema(BaseModel):
    name: str
    books: List[BookUpdate]


class BookUpdateSchema(BaseModel):
    name: str
    page_numbers: int
    author_id: uuid.UUID = None
