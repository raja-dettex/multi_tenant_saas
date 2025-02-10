from fastapi import APIRouter, Depends
from app.db.mongo import get_audit_logs_collection
from ..models.models import User
from ..models.mongo_models import AuditLogModel
from app.utils.auth import get_current_user
from ..utils.audit_logs import find_logs_by_user
from typing import List
from pydantic import BaseModel
from datetime import datetime
audit_logs_router = APIRouter()

class AuditLogResponse(BaseModel):
    user_email: str
    tenant: str
    action: str
    endpoint: str
    ip_address: str
    user_agent: str
    timestamp: datetime


@audit_logs_router.get("/audit/logs", response_model=List[AuditLogResponse])
def audit_logs(current_user : User =  Depends(get_current_user)):
    audit_logs: List[AuditLogModel] = find_logs_by_user(current_user.email)
    return [AuditLogResponse(**log) for log in audit_logs]
