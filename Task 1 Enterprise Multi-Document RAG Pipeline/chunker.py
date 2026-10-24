from langchain_text_splitters import RecursiveCharacterTextSplitter

class EnterpriseChunker:
    """Performs semantic chunking while preserving business metadata attributes."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def chunk_documents(self, raw_docs: list[dict]) -> list[dict]:
        """Splits raw extracted documents into individual chunk objects with metadata and clean text."""
        all_chunks = []
        
        for doc_idx, doc in enumerate(raw_docs):
            content = doc.get("content", "")
            base_metadata = doc.get("metadata", {})
            
            if not content or not content.strip():
                continue
            
            splits = self.splitter.split_text(content)
            for split_idx, split_text in enumerate(splits):
                meta = {str(k): str(v) for k, v in base_metadata.items()}
                meta["chunk_index"] = str(split_idx)
                
                chunk_id = f"{base_metadata.get('source', 'doc')}_{doc_idx}_chunk_{split_idx}"
                
                all_chunks.append({
                    "text": split_text,
                    "metadata": meta,
                    "id": chunk_id
                })
                
        return all_chunks