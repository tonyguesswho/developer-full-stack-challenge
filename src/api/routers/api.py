from fastapi import APIRouter

from . import auth, author

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(author.router, prefix="", tags=["Author"])
