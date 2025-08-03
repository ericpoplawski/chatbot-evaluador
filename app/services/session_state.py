from typing import List, Dict
import uuid

class SessionState:
    def __init__(self):
        self.current_score = 0
        self.answered_questions: List[int] = []
        self.errors_by_topic: Dict[str, int] = {}
        self.finished = False

# Almacena las sesiones activas
active_sessions: Dict[str, SessionState] = {}

def create_session() -> str:
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = SessionState()
    return session_id

def get_session(session_id: str) -> SessionState:
    return active_sessions.get(session_id)

