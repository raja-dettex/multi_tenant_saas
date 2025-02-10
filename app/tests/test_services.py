from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, event
from app.models.models import Base, Tenant
from app.services.tenant_service import create_tenant
import pytest

test_db_url = "sqlite:///./test.db"
engine = create_engine(test_db_url)
testLocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(engine, "before_cursor_execute")
def skip_schema_creation(conn, cursor, statement, parameters, context, executemany):
    if "create schema" in statement.lower():
        return  # Ignore schema creation in SQLite


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = testLocalSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_tenant(db):
    tenant = create_tenant(db=db, name = "Test Corp")
    assert tenant.id is not None
    assert tenant.schema_name == "test_corp"

    result = db.query(Tenant).filter_by(schema_name=tenant.schema_name).first()

    assert result is not None
    assert result.schema_name == tenant.schema_name
