from core.database import get_db
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

api_key = APIKeyHeader(name="Bearer")

from core.security import decodeJWT


def get_user(db, token):
    user = decodeJWT(db, token)
    if not user:
        raise HTTPException(status_code=403, detail="Auth Errorrrr")
    return user


def get_current_user(token: str = Security(api_key), db: Session = Depends(get_db)):
    user = get_user(db, token)
    return user
