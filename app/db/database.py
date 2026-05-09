from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# Connection pool is created here once at startup.
# SQLAlchemy connects lazily — no actual DB connection until first query.
engine = create_engine(settings.database_url)

# autocommit=False — we control transactions explicitly.
# autoflush=False — prevents SQLAlchemy flushing before queries automatically.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class all models inherit from.
# SQLAlchemy uses this to track all tables for migrations and creation.
class Base(DeclarativeBase):
    pass
    