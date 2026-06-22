from fastapi import APIRouter

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)

# =========================================================
# Create Quiz (topic-based or global)
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
    """
    Generate a quiz based on topic or global quantum knowledge.
    """
    quiz = service.generate_quiz(payload)

    if not quiz:
        raise HTTPException(
            status_code=400,
            detail="Unable to generate quiz from given topic"
        )

    return quiz