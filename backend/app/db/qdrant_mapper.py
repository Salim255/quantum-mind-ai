from app.v1.modules.rag.dto.document_dto import DocumentDTO

class QdrantMapper:
    @staticmethod
    def to_point(doc: DocumentDTO, point_id: int):
        return {
            "id": point_id,
            "vector": doc.embedding,
            "payload": {
                "text": doc.text,
                "source": doc.metadata.source,
                "concept": doc.metadata.concept,
                "difficulty": doc.metadata.difficulty,
                "length": doc.metadata.length
            }
        }