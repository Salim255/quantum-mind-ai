from app.v1.modules.conversation.service.conversation_service import ConversationService
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from pydantic import BaseModel
from app.ai_core.structured_outputs.schemas.rag_schema import RAGResponseSchema


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


class ConversationServiceImpl(ConversationService):
    def __init__(self, memory, rag_service: RAGService):
        self.memory = memory
        self.rag_service = rag_service

    async def handle_message(self, user_id: str, message: str)-> RAGResponseSchema :
        # 1. Load conversation history
        history = self.memory.get_history(user_id)

        # 2. Run your existing RAG pipeline (correct call)
        rag_result = self.rag_service.rag_pipeline(
            QueryRequest(query=message, top_k=3)
        )

        # 3. Build conversational answer (history + RAG answer)
        final_answer = self._build_conversational_answer(
            history=history,
            user_message=message,
            rag_result=rag_result
        )

        # 4. Update memory
        self.memory.add_message(user_id, "user", message)
        self.memory.add_message(user_id, "assistant", final_answer)

        return rag_result

    def _build_conversational_answer(self, history, user_message, rag_result):
        """
        We do NOT call another LLM here.
        We simply wrap the RAG answer into a conversational format.
        """

        history_text = "\n".join(
            f"{m.role}: {m.content}" for m in history
        )
        # RAG final answer (already structured)
        answer_text = rag_result.final_answer.answer

        return f"""
        Previous conversation:
        {history_text}

        User asked:
        {user_message}

        Answer:
        {answer_text}
        """.strip()
