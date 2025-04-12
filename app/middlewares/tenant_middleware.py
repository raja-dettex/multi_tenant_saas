from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse

from ..db.session import get_db
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy import text
import sys
sys.path.append("..")
import json
class TenantMiddleWare(BaseHTTPMiddleware):
    print("here")
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        
        if request.url.path.startswith("/tenants"):
            return await call_next(request)
        
        db : Session = next(get_db())
        print(request.headers)
        tenant_name = request.headers.get('x-tenant')
        print("tenant is ", tenant_name)
        if tenant_name is None:
            return JSONResponse(content={"error" : "Tenant header missing"}, status_code=400)
        try:
            db.execute(text(f"set search_path to {tenant_name}"))
        except Exception as e:
            return JSONResponse(content={'error': 'invalid tenant'}, status_code=400)

        response = await call_next(request)
        return response
