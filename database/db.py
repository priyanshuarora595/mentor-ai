import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use a dedicated data directory for better Docker volume support
db_path = os.getenv("DATABASE_PATH", "mentor.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
