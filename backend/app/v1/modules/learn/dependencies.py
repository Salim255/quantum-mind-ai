from app.v1.modules.learn.service.learn_impl_service import LearnImplService
from app.v1.modules.learn.service.learn_service import LearnService

def get_learn_service() -> LearnService:
    return LearnImplService()