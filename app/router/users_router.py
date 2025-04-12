from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from db.session import get_db
from dto.users import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Request
from models.models import User
from services.user_service import create, get_by_name, get_all, get_by_tenant_id
from utils.auth import get_current_user
from utils.audit_logs import  log_action
from typing import List
from sqlalchemy import text

import sys
sys.path.append("..")
router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(request: Request, user: UserCreate, db: Session =  Depends(get_db)):
    header = request.headers.get('X-Tenant')
    print("header is " , header)
    #db.execute(text(f"set search_path to {header}"))
    user_resp: UserResponse = create(user, db)
    log_action(
        user_email=user_resp.email,
        tenant=request.headers.get('X-Tenant'),
        action="CREATE USER API_ACCESS",
        endpoint=str(request.url.path),
        ip_address=request.client.host if request.client else "Unknown",
        user_agent=request.headers.get("User-Agent", "Unknown")
        )
    return JSONResponse(status_code=201, content={"username": user_resp.username, "email": user_resp.email, "tenant_id": user_resp.tenant_id, "tenant_username": user_resp.tenant_username})  


@router.get("/users/{username}", response_model=UserResponse)
def get_user_by_name(request: Request, username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def get_all_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log_action(
        user_email=current_user.email,
        tenant=request.headers.get('X-Tenant'),
        action="CREATE USER API_ACCESS",
        endpoint=str(request.url.path),
        ip_address=request.client.host if request.client else "Unknown",
        user_agent=request.headers.get("User-Agent", "Unknown")
        )
    return get_all(db)


@router.get("/users/tenant/{tenant_id}")
def get_users_by_tenantId(request: Request, db: Session = Depends(get_db)):
    tenant_id = request.path_params.get('tenant_id')
    if tenant_id:
            
        log_action(
            action="CREATE USER BY TenantId API_ACCESS",
            endpoint=str(request.url.path),
            ip_address=request.client.host if request.client else "Unknown",
            user_agent=request.headers.get("User-Agent", "Unknown")
            )
        return get_by_tenant_id(db, tenant_id=int(tenant_id))
    return JSONResponse(status_code=400, content={'message': 'invalid tenant id '})


