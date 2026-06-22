from fastapi import APIRouter, Depends, HTTPException, status

from app.v1.modules.quiz.dto.quiz_dto import (
    QuizCreateRequest,
    QuizResponse,
    QuizSubmitRequest,
    QuizResultResponse,
)

from app.v1.modules.quiz.service.quiz_service import QuizService


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)



# =========================================================
# GENERATE QUIZ
# =========================================================
@router.post(
    "/generate",
    response_model=QuizResponse,
    status_code=status.HTTP_201_CREATED
)
def generate_quiz(
    payload: QuizCreateRequest,
    service: QuizService = Depends(get_quiz_service),
):
    quiz = service.generate_quiz(payload)

    if not quiz:
        raise HTTPException(
            status_code=400,
            detail="Quiz generation failed"
        )

    return quiz


# =========================================================
# GET QUIZ BY ID
# =========================================================
@router.get(
    "/{quiz_id}",
    response_model=QuizResponse
)
def get_quiz(
    quiz_id: str,
    service: QuizService = Depends(get_quiz_service),
):
    quiz = service.get_quiz(quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return quiz


# =========================================================
# SUBMIT QUIZ
# =========================================================
@router.post(
    "/submit",
    response_model=QuizResultResponse
)
def submit_quiz(
    payload: QuizSubmitRequest,
    service: QuizService = Depends(get_quiz_service),
):
    result = service.evaluate_quiz(payload)

    return result


# =========================================================
# PRACTICE MODE (RANDOM QUIZ)
# =========================================================
@router.get(
    "/practice/random",
    response_model=QuizResponse
)
def random_quiz(
    topic: str | None = None,
    service: QuizService = Depends(get_quiz_service),
):
    return service.get_random_quiz(topic)