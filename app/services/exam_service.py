from app.models.schemas import Question, StudentAnswer, QuestionFeedback, FinalGrade
from app.services.session_state import get_session
from typing import List, Optional, Union

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

# Evaluación con sesiones y devolución de nota final
def evaluate_answer(answer: StudentAnswer) -> Union[QuestionFeedback, FinalGrade]:
    session = get_session(answer.session_id)

    if session is None or session.finished:
        return FinalGrade(score=session.current_score if session else 0, comments="Session is invalid or already completed.")

    if answer.question_id in session.answered_questions:
        return QuestionFeedback(
            is_correct=False,
            explanation="This question has already been answered.",
            next_question=None
        )

    session.answered_questions.append(answer.question_id)

    correct = correct_answers.get(answer.question_id)
    is_correct = correct.lower() in answer.answer.lower()

    current_question = next((q for q in questions_db if q.id == answer.question_id), None)

    if is_correct:
        session.current_score += 1
        next_question = get_next_question(after_id=answer.question_id)
        explanation = "Correct!"
    else:
        topic = current_question.topic
        session.errors_by_topic[topic] = session.errors_by_topic.get(topic, 0) + 1
        next_question = get_question_by_topic(topic, exclude_id=answer.question_id)
        explanation = f"Incorrect. The correct answer was: {correct}."

    if next_question is None:
        session.finished = True
        total = len(questions_db)
        score_percent = (session.current_score / total) * 100

        comment = (
            "Excellent!" if score_percent >= 80 else
            "Good job, but review some topics." if score_percent >= 50 else
            "Needs improvement. Review key concepts."
        )

        return FinalGrade(
            score=score_percent,
            comments=comment
        )

    return QuestionFeedback(
        is_correct=is_correct,
        explanation=explanation,
        next_question=next_question
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
