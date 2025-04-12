from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    tenant_username: str


class UserResponse(BaseModel):
    username: str
    email: str
    password: str
    tenant_id: int
    tenant_username: str
    def __init__(self, username: str, email: str, password: str, tenant_id: int, tenant_username: str):
        super().__init__(
            username=username,
            email=email,
            password=password,
            tenant_id=tenant_id,
            tenant_username=tenant_username
        )
