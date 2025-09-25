from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# The database URL is configured via environment variables in docker-compose.yml
import os
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./books.db")

# For SQLite, connect_args is needed to allow multiple threads to access the DB
# (FastAPI workers are threads)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()