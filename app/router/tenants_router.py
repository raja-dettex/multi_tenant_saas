from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Tenant
from app.services.tenant_service import create_tenant
from pydantic import BaseModel

tenant_router = APIRouter()

# Pydantic schema for tenant creation request
class TenantCreate(BaseModel):
    name: str

# Create Tenant API
@tenant_router.post("/tenants/")
def create_tenant_api(tenant_data: TenantCreate, db: Session = Depends(get_db)):
    print(tenant_data)
    existing_tenant = db.query(Tenant).filter(Tenant.name == tenant_data.name).first()
    print(existing_tenant)
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant already exists")

    tenant = create_tenant(db, tenant_data.name)
    print(tenant)
    return {"id": tenant.id, "name": tenant.name, "schema_name": tenant.schema_name}
