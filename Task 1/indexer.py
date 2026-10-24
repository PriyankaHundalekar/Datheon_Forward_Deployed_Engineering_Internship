import chromadb
from chromadb.utils import embedding_functions

class VectorStoreIndexer:
    """Manages ChromaDB vector persistence with Cosine Similarity indexing."""
    
    def __init__(
        self, 
        collection_name: str = "enterprise_legacy_docs", 
        persist_dir: str = "./chroma_db",
        persist_directory: str = None
    ):
        # Support both parameter names for seamless compatibility
        path = persist_directory if persist_directory else persist_dir
        self.client = chromadb.PersistentClient(path=path)
        
        # Using default all-MiniLM-L6-v2 sentence transformer model built into chromadb
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Create or get collection with cosine distance metric
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"} # Enforces cosine similarity index
        )

    def add_batch(self, texts: list[str], metadatas: list[dict], ids: list[str], batch_size: int = 100):
        """Adds chunks in batches to optimize throughput and memory with automatic metadata sanitization."""
        total = len(texts)
        
        # Sanitize metadata to prevent ChromaDB empty-dict or type errors
        sanitized_metadatas = []
        for meta in metadatas:
            if not meta or not isinstance(meta, dict) or len(meta) == 0:
                sanitized_metadatas.append({"source": "unknown", "department": "General"})
            else:
                cleaned_meta = {}
                for k, v in meta.items():
                    if v is not None:
                        cleaned_meta[str(k)] = v
                if not cleaned_meta:
                    cleaned_meta = {"source": "unknown"}
                sanitized_metadatas.append(cleaned_meta)

        for i in range(0, total, batch_size):
            end_idx = min(i + batch_size, total)
            self.collection.upsert(
                documents=texts[i:end_idx],
                metadatas=sanitized_metadatas[i:end_idx],
                ids=ids[i:end_idx]
            )
        print(f"Successfully indexed {total} total chunks into ChromaDB vector store.")

    def query_with_rbac(self, query_text: str, user_department: str, user_clearance: str, n_results: int = 3):
        """Performs vector search with strict metadata filtering."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={
                "$and": [
                    {"department": {"$eq": user_department}},
                    {"access_tier": {"$eq": user_clearance}}
                ]
            }
        )
        return results