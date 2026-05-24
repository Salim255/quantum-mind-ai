expanded_queries = QueryExpansionService.expand(query)

query_embeddings = EmbeddingService.embed_queries(
    expanded_queries
)

retrieved_chunks = VectorSearchService.search(
    query,
    query_embeddings
)

reranked = RerankingService.rerank(
    query,
    retrieved_chunks
)

final_chunks = DiversityService.diversify(
    reranked
)