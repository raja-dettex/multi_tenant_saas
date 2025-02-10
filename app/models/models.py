from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    schema_name = Column(String, unique=True, nullable=False)
    users = relationship("User", back_populates="tenant")

    def __int__(self, name: str, schema_name: str):
        self.name = name
        self.schema_name = schema_name


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed password
    tenant_id = Column(Integer, ForeignKey("tenants.id"))  # Links user to a tenant

    tenant = relationship("Tenant", back_populates="users")  # Each user belongs to a tenant

    def __init__(self, username: str, email: str, password: str, tenant_id: int):
        self.username = username
        self.email = email
        self.password = password
        self.tenant_id = tenant_id

    @staticmethod
    def hash_password(password: str) ->str:
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
