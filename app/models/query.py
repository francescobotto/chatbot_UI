# app/models/query.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql_query: str = None
    response: str = None
