# app/api/endpoints.py
from fastapi import APIRouter, HTTPException
from app.models.query import QueryRequest, QueryResponse
from app.services import nlp, rag

router = APIRouter()

# NLP Query API
@router.post("/nlp-query", response_model=QueryResponse)
async def nlp_query(request: QueryRequest):
    try:
        sql_query = nlp.generate_sql_query(request.question)
        return QueryResponse(sql_query=sql_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# RAG Query API
@router.post("/rag-query", response_model=QueryResponse)
async def rag_query(request: QueryRequest):
    try:
        response = rag.generate_rag_response(request.question)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
