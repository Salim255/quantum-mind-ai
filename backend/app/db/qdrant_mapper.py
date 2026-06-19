from app.v1.modules.ingestion.dto.document_dto import DocumentDTO

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
                "section_title": doc.metadata.section_title,
                "length": doc.metadata.length
            }
        }