from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
from app.v1.modules.rag.retriever.decision_engine import (decide_retrieval_action, RetrievalAction)


class DecisionService:
      @staticmethod
      def evaluate_retrieval_confidence(
            chunks: List[RetrievalChunkDTO]
            ) ->  RetrievalAction:
            """
            Decide whether retrieval quality is sufficient.

            WHY IMPORTANT?
            --------------
            Weak retrieval causes hallucinations.

            Better to:
                say "I don't know"

            than generate misinformation.
            """
            best_score = chunks[0].hybrid_score if chunks else 0.0

            print("best_score___\n", best_score)
            return decide_retrieval_action(best_score)