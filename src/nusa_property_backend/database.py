from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from .config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from sqlalchemy import text
    from . import models
    Base.metadata.create_all(bind=engine)
    
    with engine.begin() as conn:
        conn.execute(
            text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name = 'user_profiles' AND column_name = 'user_id'
                    ) THEN
                        ALTER TABLE user_profiles 
                        ADD COLUMN user_id VARCHAR(50) REFERENCES users(id) ON DELETE CASCADE;
                    END IF;
                END $$;
            """)
        )

