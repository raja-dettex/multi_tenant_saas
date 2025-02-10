from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import init_db
from app.models.models import User
from app.utils.auth import create_token
from datetime import timedelta
from pydantic import BaseModel

auth_router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str
    tenant: str  # Tenant name to identify schema


@auth_router.post("/auth/login/")
def login_for_access_token(login_data: LoginRequest, db: Session = Depends(init_db)):
    tenant_name = login_data.tenant

    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not user.verify_password(login_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_token(
        data={"sub": user.email, "tenant": tenant_name},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"}
