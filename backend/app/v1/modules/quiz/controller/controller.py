from fastapi import APIRouter, Depends, HTTPException, status

from app.v1.modules.quiz.dto.quiz_dto import (
    QuizCreateRequest,
    QuizResponse,
    QuizSubmitRequest,
    QuizResultResponse,
)
from app.v1.modules.quiz.service.quiz_service import QuizService
from app.v1.modules.quiz.dependencies import get_quiz_service
from app.v1.modules.quiz.service.quiz_service import QuizService
from typing import Annotated


router = APIRouter(
    prefix="/quizs",
    tags=["Quiz"]
)

# =========================================================
# GENERATE QUIZ
# =========================================================
@router.post(
    "/generate",
    #response_model=QuizResponse,
    status_code=status.HTTP_201_CREATED
)
def generate_quiz(
    payload: QuizCreateRequest,
    service: Annotated[QuizService, Depends(get_quiz_service)],
):
    #quiz = service.generate_quiz(payload)

    return "Hello from generate quiz"


# =========================================================
# GET QUIZ BY ID
# =========================================================
@router.get(
    "/{quiz_id}",
    response_model=QuizResponse
)
def get_quiz(
    quiz_id: str,
    service: Annotated[QuizService, Depends(get_quiz_service)],
):
    #quiz = service.get_quiz(quiz_id)

    return  "Hello from get quiz"


# =========================================================
# SUBMIT QUIZ
# =========================================================
@router.post(
    "/submit",
    response_model=QuizResultResponse
)
def submit_quiz(
    payload: QuizSubmitRequest,
    service: Annotated[QuizService, Depends(get_quiz_service)],
):
    #result = service.evaluate_quiz(payload)

    return "Hello from evaluate quiz"


# =========================================================
# PRACTICE MODE (RANDOM QUIZ)
# =========================================================
@router.get(
    "/practice/random",
    response_model=QuizResponse
)
def random_quiz(
    topic: str | None,
    service: Annotated[ QuizService, Depends(get_quiz_service)],
):
    #return service.get_random_quiz(topic)
    return "Hello from random quiz"