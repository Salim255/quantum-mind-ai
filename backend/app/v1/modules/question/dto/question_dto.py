from enum import Enum

# ============================================================
# ENUMS
# ============================================================

class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionSource(str, Enum):
    MANUAL = "manual"
    AI = "ai"
    IMPORTED = "imported"
