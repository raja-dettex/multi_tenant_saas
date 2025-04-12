from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.models import Tenant, User
from typing import List, Tuple

class TenantResponse:
    id: int
    username: str 
    email: str
    users: List[User]
    def __init__(self, id: int, username: str, email: str, users: List[User]):
        self.username = username
        self.email = email
        self.users = users
        self.id = id
def create_tenant(db: Session, username: str, email: str, password: str) -> TenantResponse:
    tenant = db.query(Tenant).filter_by(username=username).first()
    if tenant:
        print("here")
        users = users = db.query(User).filter_by(tenant_id=tenant.id).all()
        print("users")
        print(users)
        for user in users:
            print(user.id)
        return TenantResponse(id=tenant.id, username=tenant.username, email=tenant.email, users=users)
    schema_name = username.lower().replace(" ","_")
    tenant = Tenant(username=username, schema_name=schema_name , email=email, password=password)
    print(tenant)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
        
    db.execute(text(f"create schema if not exists {schema_name};"))
    db.commit()
    return TenantResponse(id=tenant.id, username=tenant.username, email=tenant.email, users=[])
