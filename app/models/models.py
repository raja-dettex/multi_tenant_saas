from sqlalchemy import Column, Integer, String, Index, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)  # ✅ Partition key, part of PK
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    schema_name = Column(String, nullable=False)

    users = relationship("User", back_populates="tenant")


    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    def __init__(self, username: str, schema_name: str, password: str, email: str):
        self.schema_name = schema_name
        self.password = self.hash_password(password)
        self.username = username
        self.email = email
    __table_args__ = (
        Index("idx_tenants_schema", "schema_name"),  # ✅ Index instead of unique constraint
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # ✅ Must include partition column
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    tenant_id = Column(Integer, ForeignKey(Tenant.id), nullable=False)

    tenant = relationship("Tenant", back_populates="users", foreign_keys=[tenant_id])

    def __init__(self, username: str, email: str, password: str, tenant_id: int):
        self.username = username
        self.email = email
        self.password = password
        self.tenant_id = tenant_id

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    __table_args__ = (
        Index("idx_users_tenant", "tenant_id"),  # ✅ Index for fast queries
    )
