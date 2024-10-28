# /app/db/crud.py

from app.db import get_db
from sqlalchemy import text

def save_feedback(feedback: str):
    db = get_db()
    query = text("INSERT INTO feedback (comment) VALUES (:feedback)")
    db.execute(query, {'feedback': feedback})
    db.commit()
