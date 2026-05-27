from typing import AsyncGenerator, Optional
import json
import logging
from app.v1.modules.conversation.service.conversation_service import ConversationService
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from pydantic import BaseModel
from app.v1.modules.conversation.schema.conversation_schema import ConversationResponse


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

logger = logging.getLogger(__name__)

class ConversationServiceImpl(ConversationService):
    def __init__(self, memory, rag_service: RAGService):
        self.memory = memory
        self.rag_service = rag_service

    async def stream_message(  self, 
            user_id: str,
            message: str, 
            conversation_id: Optional[str] = None
            )-> AsyncGenerator[str, None]:
            # 2. Run your existing RAG pipeline (correct call)
            stream = self.rag_service.rag_stream_pipeline(
                QueryRequest(query=message, top_k=3)
            )
            try:
                async for chunk in stream:

                    yield f"data: {json.dumps(chunk)}\n\n"

                yield "event: done\ndata: [DONE]\n\n"
    
            except Exception as e:

                error_payload = {
                    "type": "error",
                    "message": "Streaming failed"
                }

                logger.exception(f"Streaming error: {e}")

                yield f"event: error\ndata: {json.dumps(error_payload)}\n\n"

                
           
        

    async def handle_message(
            self, 
            user_id: str,
            message: str, 
            conversation_id: Optional[str] = None
            )-> ConversationResponse:
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

        return ConversationResponse(
            answer=rag_result,
            memory_updated=True,
            conversation_id=conversation_id
        )

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
