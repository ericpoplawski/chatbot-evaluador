from fastapi import APIRouter
from app.models.schemas import StudentAnswer, QuestionFeedback
from app.services.exam_service import evaluate_answer

router = APIRouter()

@router.post("/chat", response_model=QuestionFeedback)
def chat(answer: StudentAnswer):
    feedback = evaluate_answer(answer)
    return feedback