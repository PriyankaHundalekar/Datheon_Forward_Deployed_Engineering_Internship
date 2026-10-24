import os
import shutil
import time
from extractors import DocumentExtractor
from chunker import EnterpriseChunker
from indexer import VectorStoreIndexer

def setup_mock_data():
    """Ensure mock supporting files exist for CSV and Markdown ingestion."""
    os.makedirs("data", exist_ok=True)
    
    md_path = "data/engineering_arch.md"
    if not os.path.exists(md_path):
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Enterprise Cloud Architecture\n\nAll microservices deploy via Docker containers into secure client VPCs. Monitoring is handled via Prometheus and Grafana.")
            
    csv_path = "data/employee_directory.csv"
    if not os.path.exists(csv_path):
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("EmployeeID,Name,Role,Email,Department,AccessTier\n102,Bob Jones,Security Lead,bob@client.com,Engineering,Tier-1")

def clean_text_content(raw_content) -> str:
    """Extracts only readable plain text strings while filtering out nested dicts and ID strings."""
    if isinstance(raw_content, str):
        return raw_content
        
    extracted_strings = []
    
    # If the chunk content is a list
    if isinstance(raw_content, list):
        for item in raw_content:
            if isinstance(item, str):
                # Ignore chunk ID strings (e.g., 'COMPANY POLICY MANUAL.pdf_0_chunk_0')
                if "_chunk_" in item:
                    continue
                extracted_strings.append(item)
            elif isinstance(item, dict):
                # If nested dict has page_content or text key, extract that string
                val = item.get("page_content") or item.get("text") or item.get("content")
                if val and isinstance(val, str) and "_chunk_" not in val:
                    extracted_strings.append(val)
                    
    elif isinstance(raw_content, dict):
        val = raw_content.get("page_content") or raw_content.get("text") or raw_content.get("content")
        if val and isinstance(val, str) and "_chunk_" not in val:
            extracted_strings.append(val)

    return " ".join(extracted_strings).strip()

def main():
    print("=" * 60)
    print("🚀 INITIALIZING TASK 1: VECTOR ETL PIPELINE")
    print("=" * 60)
    
    # 1. Setup sample data environment
    setup_mock_data()
    
    # 2. Extraction Phase
    print("\n[1/3] Extracting legacy documents...")
    raw_docs = []
    
    # PDF Extraction
    pdf_path = "data/COMPANY POLICY MANUAL.pdf"
    if os.path.exists(pdf_path):
        raw_docs.extend(DocumentExtractor.extract_pdf(pdf_path, department="Executive", access_tier="Tier-1"))
    
    # Markdown Extraction (Engineering department)
    md_path = "data/engineering_arch.md"
    if os.path.exists(md_path):
        raw_docs.extend(DocumentExtractor.extract_markdown(md_path, department="Engineering", access_tier="Tier-1"))
    
    # CSV Extraction (Engineering / Operations directory)
    csv_path = "data/employee_directory.csv"
    if os.path.exists(csv_path):
        raw_docs.extend(DocumentExtractor.extract_csv(csv_path, department="Engineering", access_tier="Tier-1"))
    
    print(f"Extracted {len(raw_docs)} source documents successfully.")
    
    # 3. Semantic Chunking Phase
    print("\n[2/3] Performing semantic chunking & metadata enrichment...")
    chunker = EnterpriseChunker(chunk_size=500, chunk_overlap=50)
    chunks = chunker.chunk_documents(raw_docs)
    print(f"Generated {len(chunks)} semantic chunks with preserved attributes.")
    
    # 4. Indexing into ChromaDB Phase with Benchmarking
    print("\n[3/3] Indexing into ChromaDB vector store with Cosine Index...")
    indexer = VectorStoreIndexer(collection_name="enterprise_docs", persist_dir="./chroma_db")
    
    texts = []
    metadatas = []
    
    for i, c in enumerate(chunks):
        # Handle dict vs object document structures
        if isinstance(c, dict):
            raw_text = c.get("text") or c.get("page_content") or ""
            meta = c.get("metadata", {})
        else:
            raw_text = getattr(c, "page_content", getattr(c, "text", str(c)))
            meta = getattr(c, "metadata", {})
            
        # Clean text snippet
        text_str = clean_text_content(raw_text).strip()
        if not text_str:
            continue
            
        # Ensure metadata contains required fields
        if not isinstance(meta, dict) or not meta:
            meta = {
                "source": "COMPANY POLICY MANUAL.pdf",
                "department": "Executive",
                "access_tier": "Tier-1",
                "page": "N/A"
            }
        else:
            meta.setdefault("source", "COMPANY POLICY MANUAL.pdf")
            meta.setdefault("department", "Executive")
            meta.setdefault("access_tier", "Tier-1")
            meta.setdefault("page", "N/A")
            
        # Standardize metadata values for ChromaDB compatibility
        clean_meta = {str(k): (str(v) if v is not None else "N/A") for k, v in meta.items()}
        
        texts.append(text_str)
        metadatas.append(clean_meta)
            
    ids = [f"chunk_{i}" for i in range(len(texts))]
    
    # Execute batch insertion with timing benchmark
    start_time = time.time()
    indexer.add_batch(texts=texts, metadatas=metadatas, ids=ids, batch_size=100)
    elapsed_time = time.time() - start_time
    
    # Print benchmarking report
    print("-" * 50)
    print("📊 BATCH INGESTION BENCHMARK RESULTS")
    print(f"  • Total Chunks Indexed: {len(texts)}")
    print(f"  • Batch Execution Time: {elapsed_time:.4f} seconds")
    print(f"  • Ingestion Rate:       {len(texts) / elapsed_time if elapsed_time > 0 else 0:.2f} chunks/sec")
    print("-" * 50)
    
    # 5. Interactive Runtime Query System
    print("\n" + "=" * 60)
    print("🤖 INTERACTIVE RAG QUERY SYSTEM (Type 'exit' to quit)")
    print("=" * 60)
    
    while True:
        try:
            user_query = input("\n💬 Enter your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting query loop. Goodbye!")
            break
            
        if not user_query:
            continue
        if user_query.lower() == 'exit':
            print("Exiting query loop. Goodbye!")
            break
            
        # Query ChromaDB vector database
        query_result = indexer.collection.query(
            query_texts=[user_query],
            n_results=3
        )
        
        print(f"\n🔍 Results for: '{user_query}'")
        documents = query_result.get('documents', [[]])[0]
        metadatas_res = query_result.get('metadatas', [[]])[0]
        distances = query_result.get('distances', [[]])[0]
        
        if not documents:
            print("  No matching documents found.")
        else:
            for idx, doc in enumerate(documents):
                meta = metadatas_res[idx] if idx < len(metadatas_res) else {}
                distance = distances[idx] if idx < len(distances) else 0.0
                
                source_file = meta.get('source', 'COMPANY POLICY MANUAL.pdf')
                page_info = meta.get('page', meta.get('row_index', 'N/A'))
                dept = meta.get('department', 'Executive')
                tier = meta.get('access_tier', 'Tier-1')
                
                print(f"\n  [{idx+1}] Source File: {source_file} (Page/Row: {page_info})")
                print(f"      Cosine Distance Score: {distance:.4f} (Lower = Higher Similarity)")
                print(f"      Department: {dept} | Tier: {tier}")
                print(f"      Snippet: {doc[:250]}...")

if __name__ == "__main__":
    main()