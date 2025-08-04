from app.models.schemas import Question, StudentAnswer, QuestionFeedback, FinalGrade
from app.services.session_state import get_session
from typing import List, Optional, Union
import random

# Base de preguntas (extendida)
questions_db = [
    # Tema: general
    Question(id=1, text="When did World War II start?", topic="general"),
    Question(id=2, text="Which countries were part of the Axis powers?", topic="general"),
    Question(id=3, text="What event triggered Britain and France to declare war?", topic="general"),

    # Tema: eastern_front
    Question(id=4, text="When did Nazi Germany invade the Soviet Union?", topic="eastern_front"),
    Question(id=5, text="What was Operation Barbarossa?", topic="eastern_front"),
    Question(id=6, text="Which Soviet city resisted siege for over 2 years?", topic="eastern_front"),

    # Tema: western_front
    Question(id=7, text="What was the purpose of the D-Day invasion?", topic="western_front"),
    Question(id=8, text="Where did the D-Day landings take place?", topic="western_front"),

    # Tema: pacific
    Question(id=9, text="What attack led the US to enter WWII?", topic="pacific"),
    Question(id=10, text="Which two cities were targeted by atomic bombs?", topic="pacific"),

    # Tema: holocaust
    Question(id=11, text="What was the Holocaust?", topic="holocaust"),
    Question(id=12, text="What was Auschwitz?", topic="holocaust"),

    # Tema: africa
    Question(id=13, text="Who led the Afrika Korps?", topic="africa"),
    Question(id=14, text="What countries saw major battles in North Africa?", topic="africa"),
]

# Respuestas correctas
correct_answers = {
    1: "1939",
    2: "Germany, Italy, Japan",
    3: "Invasion of Poland",
    4: "1941",
    5: "Invasion of the Soviet Union",
    6: "Leningrad",
    7: "Liberate Western Europe",
    8: "Normandy",
    9: "Attack on Pearl Harbor",
    10: "Hiroshima and Nagasaki",
    11: "Genocide of Jews and minorities",
    12: "Nazi concentration and extermination camp",
    13: "Erwin Rommel",
    14: "Egypt and Libya",
}

# Evaluación con sesiones y devolución de nota final o próximo paso

def evaluate_answer(answer: StudentAnswer) -> Union[QuestionFeedback, FinalGrade]:
    session = get_session(answer.session_id)

    if session is None or session.finished:
        return FinalGrade(score=session.current_score if session else 0, comments="Session is invalid or already completed.")

    if answer.question_id in session.answered_questions:
        next_question = get_random_question_by_other_topic("", session.answered_questions)

        if next_question:
            return QuestionFeedback(
                is_correct=False,
                explanation="This question has already been answered.",
                next_question=next_question,
                next_action_comment="That question was already answered. Here's a new one to continue."
            )
        else:
            session.finished = True
            total = len(questions_db)
            score_percent = (session.current_score / total) * 100
            feedback = (
                "Excellent!" if score_percent >= 80 else
                "Good job, but review some topics." if score_percent >= 50 else
                "Needs improvement. Review key concepts."
            )
            return FinalGrade(score=score_percent, comments=feedback)

    session.answered_questions.append(answer.question_id)

    correct = correct_answers.get(answer.question_id)
    is_correct = correct.lower() in answer.answer.lower()

    current_question = next((q for q in questions_db if q.id == answer.question_id), None)

    if is_correct:
        session.current_score += 1
        next_question = get_random_question_by_other_topic(current_question.topic, session.answered_questions)
        explanation = "Correct!"
        comment = (
            "We are moving on to a new topic because your answer was correct."
            if next_question else "All questions completed. Calculating final grade."
        )
    else:
        topic = current_question.topic
        session.errors_by_topic[topic] = session.errors_by_topic.get(topic, 0) + 1
        next_question = get_random_question_by_topic(topic, session.answered_questions)

        if next_question:
            comment = "We will continue with more questions on this topic to reinforce it."
        else:
            next_question = get_random_question_by_other_topic(topic, session.answered_questions)
            if next_question:
                comment = "No more questions on this topic. Moving to a new topic."
            else:
                session.finished = True
                total = len(questions_db)
                score_percent = (session.current_score / total) * 100
                feedback = (
                    "Excellent!" if score_percent >= 80 else
                    "Good job, but review some topics." if score_percent >= 50 else
                    "Needs improvement. Review key concepts."
                )
                return FinalGrade(score=score_percent, comments=feedback)

        explanation = f"Incorrect. The correct answer was: {correct}."

    return QuestionFeedback(
        is_correct=is_correct,
        explanation=explanation,
        next_question=next_question,
        next_action_comment=comment
    )


def get_random_question_by_topic(topic: str, exclude_ids: List[int]) -> Optional[Question]:
    candidates = [q for q in questions_db if q.topic == topic and q.id not in exclude_ids]
    return random.choice(candidates) if candidates else None


def get_random_question_by_other_topic(current_topic: str, exclude_ids: List[int]) -> Optional[Question]:
    candidates = [q for q in questions_db if q.topic != current_topic and q.id not in exclude_ids]
    return random.choice(candidates) if candidates else None
