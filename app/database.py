from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

localsession = sessionmaker(autoflush=False, autocommit=False, bind=engine)