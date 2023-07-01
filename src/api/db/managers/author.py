import random
import string
from datetime import datetime
from typing import Optional
from uuid import UUID

from db.managers.base import BaseManager
from db.models.authors import Author
from db.models.books import Book
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class AuthorManager(BaseManager[Author]):
    def create(self, db: Session, obj_in) -> Author:
        try:
            author_obj = self.model(name=obj_in["name"])
            for book_data in [book.dict() for book in obj_in["books"]]:
                db_book = Book(
                    name=book_data["name"], page_numbers=book_data["page_numbers"]
                )
                author_obj.books.append(db_book)
                db.add(db_book)
            db.add(author_obj)
            db.commit()
            db.refresh(author_obj)
            return author_obj
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create author")

    def get_all_authors(self, db: Session, page, size):
        try:
            authors = (
                db.query(self.model)
                .order_by(self.model.updated_at.desc())
                .offset((page - 1) * size)
                .limit(size)
                .all()
            )
            return authors
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occured")

    def get_by_author_id(self, db: Session, author_id: UUID) -> Author:
        try:
            author = db.query(self.model).filter(self.model.id == author_id).first()
            return author
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occured")


class BookManager(BaseManager[Book]):
    def get_all_books(self, db: Session, page, size):
        try:
            books = db.query(self.model).offset((page - 1) * size).limit(size).all()
            return books
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occured")

    def get_by_book_id(self, db: Session, book_id: UUID) -> Book:
        try:
            book = db.query(self.model).filter(self.model.id == book_id).first()
            # print(book.author, "llllll")
            return book
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occured")

    def create(self, db: Session, obj_in) -> Book:
        try:
            print(obj_in, "aaaaaaa")
            book_obj = self.model(**obj_in.dict())
            db.add(book_obj)
            db.commit()
            db.refresh(book_obj)
            return book_obj
        except Exception as e:
            print(e, "tttttttt")
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create author")


author_manager = AuthorManager(Author)
book_manager = BookManager(Book)
