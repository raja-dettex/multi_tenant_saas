from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import init_db, get_db
from models.models import User
import os

oauth2scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
secret = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict, expires_delta: Optional[timedelta]=None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(payload=data, key=secret, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="expired signature")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Security(oauth2scheme), db: Session=Depends(get_db)) -> User:
    payload = verify_token(token)
    email = payload['sub']
    tenant = payload['tenant']
    if email is None or tenant is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email==email).first()

    if user is None:
        raise HTTPException(status_code=401, detail='user not found')
    return user
