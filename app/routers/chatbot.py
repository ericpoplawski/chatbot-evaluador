from fastapi import APIRouter
from pydantic import BaseModel
from app.models.schemas import StudentAnswer, ChatResponse
from app.services.exam_service import evaluate_answer
from app.services.session_state import create_session

router = APIRouter()

# Endpoint para iniciar una sesión
class SessionStartResponse(BaseModel):
    session_id: str

@router.post("/start", response_model=SessionStartResponse)
def start_session():
    session_id = create_session()
    return SessionStartResponse(session_id=session_id)

# Endpoint para responder preguntas
@router.post("/chat", response_model=ChatResponse)
def chat(answer: StudentAnswer):
    feedback = evaluate_answer(answer)
    return feedback