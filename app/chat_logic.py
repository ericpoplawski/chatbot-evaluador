from app.models.schemas import Question, StudentAnswer, QuestionFeedback

# Sample questions
QUESTIONS = [
    Question(id=1, text="In what year did World War II begin?", topic="start"),
    Question(id=2, text="Which country was invaded by Germany in 1939?", topic="start"),
    Question(id=3, text="Which country was invaded by Germany in Operation Barbarossa?", topic="USSR"),
    Question(id=4, text="In what year was Operation Barbarossa?", topic="USSR"),
]

# Correct answers
CORRECT_ANSWERS = {
    1: "1939",
    2: "Poland",
    3: "Soviet Union",
    4: "1941"
}

def evaluate_answer(answer: StudentAnswer) -> QuestionFeedback:
    correct_answer = CORRECT_ANSWERS.get(answer.question_id)
    is_correct = answer.answer.strip().lower() == correct_answer.lower()

    explanation = (
        "Correct! That is the expected answer." if is_correct
        else f"Incorrect. The correct answer was: {correct_answer}."
    )

    topic = next((q.topic for q in QUESTIONS if q.id == answer.question_id), "general")

    if not is_correct:
        # Look for another question from the same topic
        next_questions = [q for q in QUESTIONS if q.topic == topic and q.id != answer.question_id]
    else:
        # Look for any other question not yet asked
        next_questions = [q for q in QUESTIONS if q.id != answer.question_id]

    next_question = next_questions[0] if next_questions else None

    return QuestionFeedback(
        is_correct=is_correct,
        explanation=explanation,
        next_question=next_question
    )