from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from core import security
from core.config import settings
from core.database import get_db
from db.managers.author import author_manager, book_manager
from db.models.authors import Author
from db.models.books import Book
from db.models.users import User
from deps import get_current_user
from schemas.authors import (
    AuthorCreateSchema,
    AuthorResponseSchema,
    AuthorUpdateSchema,
    BookCreateSchema,
    BookResponseSchema,
    BookUpdateSchema,
)
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/author", response_model=AuthorResponseSchema, status_code=HTTPStatus.CREATED
)
async def create_author(author: AuthorCreateSchema, db: Session = Depends(get_db)):
    try:
        created_author = author_manager.create(db, author.__dict__)

        return AuthorResponseSchema(
            name=created_author.name,
            id=created_author.id,
            book_count=len(created_author.books),
            books=created_author.books,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error Occurred")


@router.get(
    "/authors", response_model=List[AuthorResponseSchema], status_code=HTTPStatus.OK
)
async def get_all_authors(
    page: int = Query(1, gt=0),
    page_size: int = Query(100, gt=0),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        authors = author_manager.get_all_authors(db, page, page_size)
        author_responses = [
            AuthorResponseSchema(
                id=author.id,
                name=author.name,
                book_count=len(author.books),
                books=author.books,
            )
            for author in authors
        ]
        return author_responses
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred")


@router.get(
    "/author/{author_id}",
    response_model=AuthorResponseSchema,
    status_code=HTTPStatus.OK,
)
async def get_author(author_id: UUID, db: Session = Depends(get_db)):
    try:
        author = author_manager.get_by_author_id(db, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return AuthorResponseSchema(
            id=author.id,
            name=author.name,
            book_count=len(author.books),
            books=author.books,
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="An error occurred"
        )


@router.put("/authors/{author_id}", status_code=HTTPStatus.OK)
async def update_author(
    author_id: UUID, author_update: AuthorUpdateSchema, db: Session = Depends(get_db)
):
    try:
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Author not found"
            )

        # Update author's name
        author.name = author_update.name

        # Update or add books
        updated_books = []
        for book_update in author_update.books:
            book = db.query(Book).filter(Book.id == book_update.id).first()
            if book:
                # Update existing book
                book.name = book_update.name
                book.page_numbers = book_update.page_numbers
            updated_books.append(book)

        # Remove deleted books associated with the author
        deleted_books = [book for book in author.books if book not in updated_books]
        for deleted_book in deleted_books:
            db.delete(deleted_book)

        # Remove deleted books associated with the author
        author.books = updated_books

        db.commit()
        db.refresh(author)
        return author
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An error occurred",
        )


@router.post("/book", response_model=BookResponseSchema, status_code=HTTPStatus.CREATED)
async def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    try:
        new_book = book_manager.create(db, book)
        return new_book
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An error occurred",
        )


@router.get(
    "/book/{book_id}",
    response_model=BookResponseSchema,
    status_code=HTTPStatus.OK,
)
async def get_book(book_id: UUID, db: Session = Depends(get_db)):
    try:
        book = book_manager.get_by_book_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookResponseSchema(
            id=book.id,
            name=book.name,
            page_numbers=book.page_numbers,
            author=book.author,
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="An error occurred"
        )


@router.get(
    "/books", response_model=List[BookResponseSchema], status_code=HTTPStatus.OK
)
async def get_all_books(
    page: int = Query(1, gt=0),
    page_size: int = Query(100, gt=0),
    db: Session = Depends(get_db),
):
    try:
        books = book_manager.get_all_books(db, page, page_size)
        books_res = [
            BookResponseSchema(
                id=book.id,
                name=book.name,
                page_numbers=book.page_numbers,
                author=book.author,
            )
            for book in books
        ]
        return books_res
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred")


@router.put("/books/{book_id}", status_code=HTTPStatus.OK)
async def update_book(
    book_id: UUID, book_update: BookUpdateSchema, db: Session = Depends(get_db)
):
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Book not found"
            )

        # Update book attributes
        book.name = book_update.name
        book.page_numbers = book_update.page_numbers

        # Update author if provided
        if book_update.author_id:
            author = db.query(Author).filter(Author.id == book_update.author_id).first()
            if not author:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="Author not found"
                )
            book.author = author

        db.commit()
        db.refresh(book)
        return book
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An error occurred",
        )
