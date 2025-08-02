from app.models.schemas import Question, StudentAnswer, QuestionFeedback
from typing import List, Optional

# Base de preguntas (mock)
questions_db = [
    Question(id=1, text="When did World War II start?", topic="general"),
    Question(id=2, text="Which countries were part of the Axis powers?", topic="general"),
    Question(id=3, text="When did Nazi Germany invade the Soviet Union?", topic="eastern_front"),
    Question(id=4, text="What was Operation Barbarossa?", topic="eastern_front"),
    Question(id=5, text="What was the purpose of the D-Day invasion?", topic="western_front"),
]

# Respuestas correctas (clave = id de la pregunta)
correct_answers = {
    1: "1939",
    2: "Germany, Italy, Japan",
    3: "1941",
    4: "Invasion of the Soviet Union",
    5: "Liberate Western Europe",
}

# Lógica para corregir la respuesta del alumno
def evaluate_answer(answer: StudentAnswer) -> QuestionFeedback:
    correct = correct_answers.get(answer.question_id)
    is_correct = correct.lower() in answer.answer.lower()

    current_question = next((q for q in questions_db if q.id == answer.question_id), None)
    
    if is_correct:
        next_question = get_next_question(after_id=answer.question_id)
        return QuestionFeedback(
            is_correct=True,
            explanation="Correct!",
            next_question=next_question
        )
    else:
        follow_up = get_question_by_topic(current_question.topic, exclude_id=answer.question_id)
        return QuestionFeedback(
            is_correct=False,
            explanation=f"Incorrect. The correct answer was: {correct}.",
            next_question=follow_up
        )

def get_next_question(after_id: int) -> Optional[Question]:
    for q in questions_db:
        if q.id > after_id:
            return q
    return None

def get_question_by_topic(topic: str, exclude_id: int) -> Optional[Question]:
    for q in questions_db:
        if q.topic == topic and q.id != exclude_id:
            return q
    return None
