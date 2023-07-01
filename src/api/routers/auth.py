from http import HTTPStatus

from core import security
from core.config import settings
from core.database import get_db
from db.managers.users import jwt_manager, user_manager
from db.models.users import User
from deps import get_current_user
from schemas.users import LoginResponseSchema, LoginUserSchema
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", response_model=LoginResponseSchema, status_code=HTTPStatus.OK)
async def login_user(user_in: LoginUserSchema, db: Session = Depends(get_db)):
    user = user_manager.get_by_username(db, user_in.username)
    if not user or not security.verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid username or password",
        )

    existing_jwt = jwt_manager.get_by_user_id(db, user.id)
    if existing_jwt:
        jwt_manager.delete(db, existing_jwt)

    access = security.create_access_token(
        {
            "user_id": str(user.id),
            "username": user.username,
        }
    )
    refresh = security.create_refresh_token()

    jwt_manager.create(db, {"user_id": user.id, "access": access, "refresh": refresh})

    return {
        "message": "Login successful",
        "data": {"access": access, "refresh": refresh},
    }
