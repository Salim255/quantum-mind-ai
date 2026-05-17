from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, docs: list) -> list:
    pairs = [(query, d["text"]) for d in docs]
    scores = reranker.predict(pairs)

    # Attach scores
    for doc, score in zip(docs, scores):
        doc["rerank_score"] = float(score)

    # Sort by rerank score
    docs.sort(key=lambda x: x["rerank_score"], reverse=True)

    return docs
