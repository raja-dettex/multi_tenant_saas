from typing import List

from sqlalchemy.orm import Session
from dto.users import UserResponse, UserCreate
from models.models import User, Tenant
import sys
sys.path.append("..")

def create(user_create: UserCreate, db: Session) -> UserResponse:
    user = get_by_name(user_create.username, db)
    if user:
        return user
    tenant = db.query(Tenant).filter_by(schema_name=user_create.tenant_username).first()
    user = User(
        username= user_create.username,
        email = user_create.email,
        password= User.hash_password(user_create.password),
        tenant_id=tenant.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse(
        username=user.username,
        email=user.email,
        password=user.password,
        tenant_id=user.tenant_id,
        tenant_username=tenant.username
    )


def get_by_name(name: str, db: Session) -> UserResponse:
    user = db.query(User).filter_by(username=name).first()
    if user is None:
        return None
    tenant = db.query(Tenant).filter_by(id=user.tenant_id).first()
    return UserResponse(
        username=user.username,
        email=user.email,
        password=user.password,
        tenant_id=user.tenant_id,
        tenant_username= tenant.username
    )


def get_all(db : Session ) -> List[UserResponse]:
    users = db.query(User).all()
    return [UserResponse(
        username=user.username,
        email = user.email,
        password=user.password,
        tenant_id=user.tenant_id
    ) for user in users if user is not None]
