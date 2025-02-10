from fastapi import APIRouter, Depends, HTTPException
from ..db.session import init_db
from ..dto.users import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Request
from ..models.models import User
from ..services.user_service import create, get_by_name, get_all
from ..utils.auth import get_current_user
from ..utils.audit_logs import  log_action
from typing import List
router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(request: Request, user: UserCreate, db: Session =  Depends(init_db)):
    user_resp: UserResponse = create(user, db)
    log_action(
        user_email=user_resp.email,
        tenant=request.headers.get('X-Tenant'),
        action="CREATE USER API_ACCESS",
        endpoint=str(request.url.path),
        ip_address=request.client.host if request.client else "Unknown",
        user_agent=request.headers.get("User-Agent", "Unknown")
        )
    return user_resp


@router.get("/users/{username}", response_model=UserResponse)
def get_user_by_name(request: Request, username: str, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    user_resp : UserResponse = get_by_name(username, db)
    if user_resp is None:
        raise HTTPException(status_code=404, detail="user not found")
    log_action(
        user_email=current_user.email,
        tenant=request.headers.get('X-Tenant'),
        action="CREATE USER API_ACCESS",
        endpoint=str(request.url.path),
        ip_address=request.client.host if request.client else "Unknown",
        user_agent=request.headers.get("User-Agent", "Unknown")
        )
    return user_resp


@router.get("/users/", response_model=List[UserResponse])
def get_all_users(request: Request, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    log_action(
        user_email=current_user.email,
        tenant=request.headers.get('X-Tenant'),
        action="CREATE USER API_ACCESS",
        endpoint=str(request.url.path),
        ip_address=request.client.host if request.client else "Unknown",
        user_agent=request.headers.get("User-Agent", "Unknown")
        )
    return get_all(db)


