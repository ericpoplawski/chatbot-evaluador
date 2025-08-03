from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    id: int
    text: str
    topic: str

class StudentAnswer(BaseModel):
    session_id: str
    question_id: int
    answer: str

class QuestionFeedback(BaseModel):
    is_correct: bool
    explanation: Optional[str] = None
    next_question: Optional[Question] = None

class FinalGrade(BaseModel):
    score: float
    comments: Optional[str] = None