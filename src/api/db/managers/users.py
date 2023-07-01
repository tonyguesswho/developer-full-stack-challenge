import random
import string
from datetime import datetime
from typing import Optional
from uuid import UUID

from core.security import get_password_hash
from db.managers.base import BaseManager
from db.models.users import Jwt, User
from sqlalchemy.orm import Session


class UserManager(BaseManager[User]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        user = db.query(self.model).filter_by(username=username).first()
        return user

    def create(self, db: Session, obj_in) -> User:
        obj_in.update({"password": get_password_hash(obj_in["password"])})
        user_obj = self.model(**obj_in)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj


class JwtManager(BaseManager[Jwt]):
    def get_by_user_id(self, db: Session, user_id: UUID) -> Optional[Jwt]:
        jwt = db.query(self.model).filter_by(user_id=user_id).first()
        return jwt

    def get_by_refresh(self, db: Session, refresh: str) -> Optional[Jwt]:
        jwt = db.query(self.model).filter_by(refresh=refresh).first()
        return jwt


# How to use
user_manager = UserManager(User)
jwt_manager = JwtManager(Jwt)
