from db.mongo import get_audit_logs_collection
from models.mongo_models import AuditLogModel
from typing import List
audit_logs_collection = get_audit_logs_collection()


def log_action(user_email: str, tenant: str, action: str, endpoint: str, ip_address: str, user_agent: str):
    log_entry = AuditLogModel(
        user_email=user_email,
        tenant=tenant,
        action=action,
        endpoint=endpoint,
        ip_address=ip_address,
        user_agent=user_agent
    ).model_dump()
    print(audit_logs_collection)
    audit_logs_collection.insert_one(log_entry)


def find_logs_by_user(email: str) -> List[AuditLogModel]:
    return list(audit_logs_collection.find({'user_email': email}))
