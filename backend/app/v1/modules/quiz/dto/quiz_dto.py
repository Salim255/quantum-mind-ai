from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# =========================================================
# QUESTION DTO
# =========================================================

class QuizQuestionDTO(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: str

    topic: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"] = "easy"

    explanation: Optional[str] = None


# =========================================================
# QUIZ CREATE REQUEST
# =========================================================

class QuizCreateRequest(BaseModel):
    topic: Optional[str] = Field(
        default=None,
        description="Quantum topic like entanglement, measurement, superposition"
    )

    difficulty: Optional[Literal["easy", "medium", "hard"]] = "easy"

    number_of_questions: int = Field(
        default=5,
        ge=1,
        le=50
    )

    mode: Literal["topic", "global"] = "topic"


# =========================================================
# QUIZ RESPONSE (returned to frontend)
# =========================================================

class QuizResponse(BaseModel):
    quiz_id: str
    title: str

    topic: Optional[str] = None
    mode: Literal["topic", "global"]

    questions: List[QuizQuestionDTO]

    created_at: datetime


# =========================================================
# SUBMIT ANSWERS DTO
# =========================================================

class QuizAnswerDTO(BaseModel):
    question_id: str
    selected_answer: str


class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: List[QuizAnswerDTO]


# =========================================================
# QUIZ RESULT RESPONSE
# =========================================================

class QuizResultResponse(BaseModel):
    quiz_id: str

    score: float  # percentage 0–100
    correct_count: int
    total_questions: int

    wrong_questions: List[str]  # question_ids

    completed_at: datetime