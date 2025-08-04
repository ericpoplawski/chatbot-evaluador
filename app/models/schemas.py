from pydantic import BaseModel
from typing import Optional
from typing import Union

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
    next_action_comment: Optional[str] = None

class FinalGrade(BaseModel):
    score: float
    comments: Optional[str] = None

ChatResponse = Union[QuestionFeedback, FinalGrade]