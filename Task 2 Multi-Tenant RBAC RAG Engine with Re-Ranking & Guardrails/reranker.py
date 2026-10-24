from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    """Re-ranks retrieved vector chunks using a Cross-Encoder model for high precision[cite: 3]."""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        print(f"Loading Cross-Encoder model ({model_name})...")
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: list[str], metadatas: list[dict], top_k: int = 3) -> list[dict]:
        """Scores and re-ranks documents based on cross-encoder semantic relevance."""
        if not documents:
            return []
        
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)
        
        scored_results = []
        for doc, meta, score in zip(documents, metadatas, scores):
            scored_results.append({
                "document": doc,
                "metadata": meta,
                "score": float(score)
            })
        
        # Sort descending by cross-encoder score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]