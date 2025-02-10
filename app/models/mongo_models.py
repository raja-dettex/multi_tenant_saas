from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AuditLogModel(BaseModel):
    user_email: str = Field(..., example="raja@example.com")
    tenant: str = Field(..., example="test_corp")
    action: str = Field(..., example="API_ACCESS")
    endpoint: str = Field(..., example="/users/me/")
    ip_address: Optional[str] = Field(default="Unknown", example="192.168.1.10")
    user_agent: Optional[str] = Field(default="Unknown", example="Mozilla/5.0")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
