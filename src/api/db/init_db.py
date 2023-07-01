from core.database import get_db
from schemas.users import RegisterUserSchema
from core.config import settings
from db.managers.users import user_manager
from db.models.authors import Author
from db.models.books import Book
from faker import Faker
from sqlalchemy.orm import Session
import random


def create_dummy_authors(db, num_authors):
    fake = Faker()
    authors = []

    for _ in range(num_authors):
        author = Author(name=fake.name())
        db.add(author)
        authors.append(author)

    db.commit()
    return authors


def create_dummy_books(db, authors, num_books):
    fake = Faker()

    for _ in range(num_books):
        book = Book(
            name=fake.catch_phrase(),
            page_numbers=random.randint(100, 500),
            author=random.choice(authors),
        )
        db.add(book)

    db.commit()


def populate_dummy_data(db: Session):
    num_authors = 10  # Number of dummy authors to create
    num_books = 50  # Number of dummy books to create

    authors = create_dummy_authors(db, num_authors)
    create_dummy_books(db, authors, num_books)

    db.close()


def init_db(db: Session) -> None:
    user = user_manager.get_by_username(db=db, username="testuser")
    if not user:
        user_in = RegisterUserSchema(username="testuser", password="testpassword")
        user_manager.create(db=db, obj_in=user_in.dict())
    populate_dummy_data(db=db)
