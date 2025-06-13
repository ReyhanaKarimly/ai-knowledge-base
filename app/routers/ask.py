from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.qa_engine import answer_question

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask/")
def ask_question(q: Question):
    answer = answer_question(q.question)
    if not answer:
        raise HTTPException(status_code=404, detail="No documents available.")
    return answer