from app.v1.modules.quiz.service.quiz_service import QuizService

# =========================================================
# Dependency Injection
# =========================================================
def get_quiz_service() -> QuizService:
    return QuizService()