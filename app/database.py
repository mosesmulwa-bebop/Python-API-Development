from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# format for database url
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
# engine is responsible for connecting to postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# talking to sql database requires creation of a session

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind= engine)

# define base class to be extended by all other models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()