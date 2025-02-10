from typing import List

from ..db.mongo import get_audit_logs_collection
from ..models.mongo_models import AuditLogModel
from ..utils.audit_logs import log_action, find_logs_by_user


def  test_conn():
    conn = get_audit_logs_collection()
    print(conn)
    assert conn is not None


def test_insert_one():
    log_action(
        user_email='demo@gmail.com',
        tenant='demo_tenant',
        action='auth',
        endpoint='/auth/login',
        ip_address='44.124.34.56',
        user_agent='agent'
    )


def test_find_logs_by_user():
    logs : List[AuditLogModel] = find_logs_by_user('demo@gmail.com')
    print(logs)
    assert len(logs) != 0
