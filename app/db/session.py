from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models.models import Base
# Load environment variables from .env file
load_dotenv()

# Fetch the DATABASE_URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():

    Base.metadata.create_all(bind=engine)

    # with engine.begin() as conn:
    #     conn.execute(text("CREATE EXTENSION IF NOT EXISTS citus;"))
    #     conn.execute(text("SELECT * FROM citus_add_node('citus_worker1', 5432);"))
    #     conn.execute(text("SELECT * FROM citus_add_node('citus_worker2', 5432);"))
    #     conn.execute(text("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_tenant_id_fkey;"))

    #     conn.execute(text("ALTER TABLE tenants DROP CONSTRAINT IF EXISTS tenants_pkey;"))
    #     conn.execute(text("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_pkey;"))

    #     conn.execute(text("""
    #     DO $$
    #     BEGIN
    #         IF NOT EXISTS (
    #             SELECT 1 FROM pg_dist_partition
    #             WHERE logicalrelid = 'tenants'::regclass
    #         ) THEN
    #             PERFORM create_distributed_table('tenants', 'id');
    #         END IF;
    #     END
    #     $$;
    # """))

    #     conn.execute(text("""
    #         DO $$
    #         BEGIN
    #             IF NOT EXISTS (
    #                 SELECT 1 FROM pg_dist_partition
    #                 WHERE logicalrelid = 'users'::regclass
    #             ) THEN
    #                 PERFORM create_distributed_table('users', 'tenant_id');
    #             END IF;
    #         END
    #         $$;
    #     """))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
