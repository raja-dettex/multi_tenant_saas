from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    tenant_id: int


class UserResponse(BaseModel):
    username: str
    email: str
    password: str
    tenant_id: int

    def __init__(self, username: str, email: str, password: str, tenant_id: int):
        super().__init__(
            username=username,
            email=email,
            password=password,
            tenant_id=tenant_id
        )
