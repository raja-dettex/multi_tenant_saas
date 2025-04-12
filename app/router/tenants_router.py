from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Tenant
from app.services.tenant_service import create_tenant
from pydantic import BaseModel
from fastapi.responses import JSONResponse
tenant_router = APIRouter()
import json
# Pydantic schema for tenant creation request
class TenantCreate(BaseModel):
    username: str
    email: str
    password: str

# Create Tenant API
@tenant_router.post("/tenants/")
def create_tenant_api(tenant_data: TenantCreate, db: Session = Depends(get_db)):
    print(tenant_data)
    

    tenant = create_tenant(db, tenant_data.username, email=tenant_data.email, password=tenant_data.password)
    print(tenant)
    return JSONResponse(status_code=201, content={"tenant_id": tenant.id, "username": tenant.username, "email": tenant.email, 
                                                  "users": [
                                                      {"username": user.username, 
                                                       "email": user.email,} for user in tenant.users
                                                  ]})
