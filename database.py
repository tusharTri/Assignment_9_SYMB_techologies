from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
SQLALCHEMY_DATABASE_URI = os.environ.get('A9_DB_URI')

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# postgresql://postgres:database@localhost:5432/fastapi