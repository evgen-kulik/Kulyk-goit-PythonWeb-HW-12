from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:567234@localhost:5432/hw_12_postgres"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# "check_same_thread": False (тільки для SQLite!) дозволяє відкривати кілька з'єднань
# з різних потоків до однієї бази даних.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
