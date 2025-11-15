from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from ..config import DATABASE_URL
import logging

# Create the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

logger = logging.getLogger(__name__)


class User(Base):
    """User model for the database."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def init_db():
    """Initialize the database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_user(user_id: int, username: str, first_name: str = None, last_name: str = None) -> bool:
    """Add a new user to the database."""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.id == user_id).first()
        if existing_user:
            logger.info(f"User {user_id} already exists")
            return False
        
        new_user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(new_user)
        db.commit()
        logger.info(f"User {user_id} added successfully")
        return True
    except Exception as e:
        logger.error(f"Error adding user {user_id}: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def get_user(user_id: int) -> User:
    """Retrieve a user from the database."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}")
        return None
    finally:
        db.close()


def update_user_verification(user_id: int, is_verified: bool = True) -> bool:
    """Update user verification status."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_verified = is_verified
            db.commit()
            logger.info(f"User {user_id} verification updated to {is_verified}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error updating user {user_id} verification: {e}")
        db.rollback()
        return False
    finally:
        db.close()