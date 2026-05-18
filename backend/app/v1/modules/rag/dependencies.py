
from app.ai_core.rag.services.implementations.generator_service_impl import GeneratorServiceImpl
from app.ai_core.rag.services.implementations.retriever_service_impl import RetrieverServiceImpl
from app.ai_core.rag.services.interfaces.generator_service import GeneratorService
from app.ai_core.rag.services.interfaces.generator_service import GeneratorService
from app.ai_core.rag.services.interfaces.retriever_service import RetrieverService


def get_retriever_service() -> RetrieverService:
    return RetrieverServiceImpl()

def get_answer_generator_service() -> GeneratorService:
    return GeneratorServiceImpl()