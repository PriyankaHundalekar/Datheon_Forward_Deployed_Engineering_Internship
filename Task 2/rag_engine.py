import ollama
from chromadb import PersistentClient
from rbac import RBACManager
from query_rewriter import QueryRewriter
from reranker import CrossEncoderReranker

class EnterpriseRAGEngine:
    """Production-grade secure RAG engine with RBAC, query rewriting, re-ranking, and strict citation guardrails[cite: 3]."""
    
    def __init__(self, persist_dir: str = "../Task 1/chroma_db", collection_name: str = "enterprise_docs"):
        self.client = PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection(collection_name)
        self.rewriter = QueryRewriter(model_name="qwen3:4b")
        self.reranker = CrossEncoderReranker()

    def query(self, raw_query: str, username: str) -> dict:
        # 1. Fetch user RBAC profile
        user = RBACManager.get_user_profile(username)
        dept = user["department"]
        
        # 2. Query Re-writing
        expanded_query = self.rewriter.rewrite(raw_query)
        
        # 3. Secure Retrieval with RBAC Metadata Filtering[cite: 3]
        rbac_filter = RBACManager.build_filter(dept)
        
        retrieval_res = self.collection.query(
            query_texts=[expanded_query],
            n_results=10, # Fetch top 10 candidates for cross-encoder re-ranking
            where=rbac_filter
        )
        
        documents = retrieval_res.get("documents", [[]])[0]
        metadatas = retrieval_res.get("metadatas", [[]])[0]
        
        if not documents:
            return {
                "answer": f"Access Denied or No Relevant Documents Found for Department clearance: {dept}.",
                "citations": [],
                "expanded_query": expanded_query
            }

        # 4. Cross-Encoder Re-ranking[cite: 3]
        ranked_results = self.reranker.rerank(raw_query, documents, metadatas, top_k=3)
        
        # 5. Format Context Snippets with Verifiable Citations[cite: 3]
        context_blocks = []
        citations = []
        for idx, res in enumerate(ranked_results):
            doc_text = res["document"]
            meta = res["metadata"]
            source_file = meta.get("source", "Unknown")
            page_no = meta.get("page", meta.get("row_index", "N/A"))
            
            context_blocks.append(f"[Snippet {idx+1}] (Source: {source_file}, Page/Row: {page_no})\n{doc_text}")
            citations.append(f"Source: {source_file} (Page/Row: {page_no})")

        context_str = "\n\n".join(context_blocks)
        
        # 6. Strict Hallucination Guardrail & Citation Prompt[cite: 3]
        prompt = f"""You are a secure corporate AI assistant. Answer the user's question using ONLY the provided context snippets below.
        Strict Guardrails:
        1. If the answer cannot be found explicitly within the provided context snippets, state: "I do not have access to verified company documentation to answer this question." Do not fabricate information.
        2. Every factual statement or claim MUST cite its source file and page/row number.
        
        Context Snippets:
        {context_str}
        
        User Question: {raw_query}
        
        Answer:"""

        response = ollama.chat(
            model="qwen3:4b",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1}
        )
        
        answer = response["message"]["content"].strip()
        
        return {
            "answer": answer,
            "citations": citations,
            "expanded_query": expanded_query,
            "user_context": user
        }