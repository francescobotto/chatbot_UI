# /app/db/__init__.py

from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./chatbot.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

def get_db():
    return engine.connect()
