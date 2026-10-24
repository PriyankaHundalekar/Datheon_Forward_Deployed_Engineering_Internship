import ollama

class QueryRewriter:
    """Rewrites and expands raw user queries for optimized vector recall[cite: 3]."""
    
    def __init__(self, model_name: str = "qwen3:4b"):
        self.model_name = model_name

    def rewrite(self, query: str) -> str:
        prompt = f"""You are an enterprise search query expansion assistant. 
        Rewrite the following user query into a clear, information-dense search string 
        optimized for semantic vector retrieval. Output ONLY the rewritten query text without pleasantries or markdown formatting.
        
        User Query: "{query}"
        Rewritten Query:"""
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1}
            )
            rewritten = response['message']['content'].strip()
            return rewritten if rewritten else query
        except Exception as e:
            print(f"Warning: Query re-writing failed ({e}). Falling back to original query.")
            return query