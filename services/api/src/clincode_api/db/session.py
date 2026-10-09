import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://clincode:clincode_dev_2026@localhost:5432/clincode"
)

def get_engine():
    """Initializes database engine with automatic SQLite fallback if PostgreSQL is offline."""
    if DATABASE_URL.startswith("sqlite"):
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    
    try:
        pg_engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)
        # Attempt connection check
        with pg_engine.connect() as conn:
            pass
        return pg_engine
    except Exception:
        # Fallback to local SQLite database when PostgreSQL server is offline
        sqlite_url = "sqlite:///./clincode_dev.db"
        return create_engine(sqlite_url, connect_args={"check_same_thread": False})


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency for providing a SQLAlchemy database session to API routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
