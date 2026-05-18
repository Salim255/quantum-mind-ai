
from app.v1.modules.rag.services.implementations.generator_service_impl import GeneratorServiceImpl
from app.v1.modules.rag.services.implementations.retriever_service_impl import RetrieverServiceImpl
from app.v1.modules.rag.services.interfaces.generator_service import GeneratorService
from app.v1.modules.rag.services.interfaces.generator_service import GeneratorService
from app.v1.modules.rag.services.interfaces.retriever_service import RetrieverService


def get_retriever_service() -> RetrieverService:
    return RetrieverServiceImpl()

def get_answer_generator_service() -> GeneratorService:
    return GeneratorServiceImpl()