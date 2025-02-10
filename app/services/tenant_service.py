from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.models import Tenant


def create_tenant(db: Session, name: str):
    schema_name = name.lower().replace(" ","_");
    tenant = Tenant(name=name, schema_name=schema_name)
    print(tenant)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    db.execute(text(f"create schema if not exists {schema_name};"))
    db.commit()
    return tenant
