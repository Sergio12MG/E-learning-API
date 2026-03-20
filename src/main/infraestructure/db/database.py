from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 1. Load the environment variables
load_dotenv()

# 2. Get the URL to connect the DB
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False, pool_recycle=3600)

# 3. Create a session factory to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class for the SQLAlchemy models
Base = declarative_base()

# 5. To provide a DB session for each request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
