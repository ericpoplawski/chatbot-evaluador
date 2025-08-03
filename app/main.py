from fastapi import FastAPI
from app.models.schemas import StudentAnswer, QuestionFeedback
from app.chat_logic import evaluate_answer

app = FastAPI()

@app.post("/chat", response_model=QuestionFeedback)
def chat_endpoint(answer: StudentAnswer):
    return evaluate_answer(answer)
