from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from .db.session import init_db
from .middlewares.tenant_middleware import TenantMiddleWare
from .router.users_router import router
from .router.tenants_router import tenant_router
from .router.auth_router import auth_router
from .router.audit_logs_router import  audit_logs_router
from .exceptions.error_handlers import handle_integrity_error, handle_database_error, handle_general_exception, \
    rate_limit_exceeded_handler
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

app = FastAPI(title="Multi-Tenant SaaS")


@app.on_event("startup")
def migrate_schema():
    init_db()

app.add_middleware(TenantMiddleWare)
app.include_router(router=router)
app.include_router(router=tenant_router)
app.include_router(router=auth_router)
app.include_router(router=audit_logs_router)
app.add_exception_handler( IntegrityError, handle_integrity_error)
app.add_exception_handler(SQLAlchemyError, handle_database_error)
app.add_exception_handler(Exception, handle_general_exception)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
