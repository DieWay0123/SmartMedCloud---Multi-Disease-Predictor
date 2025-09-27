from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import and_, create_engine, or_

from settings import settings


engine = create_engine(settings.db_connection)
SessionLocal = sessionmaker(engine, autoflush=False)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        raise
    finally:
        db.close()