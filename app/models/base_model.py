from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from core.config import app_config

# DATABASE_URL = "postgresql+psycopg2://postgres:6b9df25125b065610f5b6db237b28690@db:5432/surepath"
    
engine = create_engine(app_config.DATABASE_URL)

SessionLocal:Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class AppEntityStatus:
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"
    
class AppStateStatus:
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class UserRoles:
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    PROVIDER = "PROVIDER"
    USER = "USER"