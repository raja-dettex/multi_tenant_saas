from fastapi import Request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi.responses import JSONResponse
import re


def handle_integrity_error(request : Request, error: IntegrityError):
    error_message = str(error.orig)
    match = re.search(r'Key \((.*?)\)=\((.*?)\) already exists', error_message)

    if match:
        key, value = match.groups()
        detail = f"Duplicate entry {key} '{value}' already exists"
    else:
        detail = "unique constraint violation occured"

    return JSONResponse(
        status_code=400,
        content={'error': detail}
    )


def handle_database_error(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"error": f"A database error occurred. Please try again later. {exc}"}
    )


def handle_general_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"Unexpected error: {str(exc)}"}
    )


from slowapi.errors import RateLimitExceeded

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Please try again later."},
    )
