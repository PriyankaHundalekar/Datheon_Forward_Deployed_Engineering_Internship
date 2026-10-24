# Task 1: Client Legacy Data Ingestion & Vector ETL Pipeline

An automated, enterprise-grade Vector ETL (Extract, Transform, Load) pipeline designed to ingest messy, multi-format corporate legacy data (PDFs, Markdown, CSVs), perform semantic chunking with Role-Based Access Control (RBAC) metadata preservation, and index vector embeddings into ChromaDB configured with Cosine Similarity. Includes automated batch processing benchmarking and an interactive runtime query interface.

---

## 📌 Features & Key Capabilities

- **Multi-Format Ingestion**: Custom modular extractors for PDF document packages, technical Markdown runbooks, and structured CSV datasets.
- **Semantic Chunking & Attribute Preservation**: Powered by `RecursiveCharacterTextSplitter` (chunk size: 500, overlap: 50), preserving metadata attributes such as `department`, `access_tier`, `source`, `page`/`row_index`, and `chunk_index`.
- **ChromaDB Vector Store Integration**: Cosine similarity space index initialization with clean string payload serialization.
- **Automated Batch Ingestion Benchmarking**: Real-time measurement of indexing performance, tracking execution timing, chunk counts, and processing throughput (chunks/sec).
- **Interactive Runtime Query System**: Built-in CLI query system to run semantic similarity searches across all indexed documents with distance scoring and metadata extraction.

---

## 📁 Repository Directory Structure

```text
Task 1/
├── chroma_db/                  # Persistent ChromaDB sqlite database & vectors
│   ├── b33cd325-8b20-4a1d-9793-ea28b03c0c71/
│   └── chroma.sqlite3
├── data/                       # Legacy input documents folder
│   ├── COMPANY POLICY MANUAL.pdf
│   ├── employee_directory.csv
│   └── engineering_arch.md
├── Outputs/                    # Execution verification screenshots
│   ├── CSV_Output1.png
│   ├── CSV_Output2.png
│   ├── Extracting_Semantic_Chunking_ChromaDB.png
│   ├── Markdown_Output1.png
│   ├── Markdown_Output2.png
│   ├── PDF_testing _Output1.png
│   ├── PDF_testing _Output2.png
│   └── PDF_testing _Output3.png
├── chunker.py                  # EnterpriseChunker logic (semantic splitting)
├── extractors.py               # DocumentExtractor class for PDF, Markdown, and CSV
├── indexer.py                  # VectorStoreIndexer class for ChromaDB lifecycle
├── main.py                     # Primary pipeline entry point & interactive CLI query loop
├── Question.txt                # Reference task query notes
├── README.md                   # Detailed project documentation
└── requirements.txt            # Python environment dependencies
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+ installed on your system.

### 1. Clone & Navigate to Project Directory
```bash
cd "Task 1"
```

### 2. Activate Virtual Environment
On Windows:
```cmd
venv\Scripts\activate
```

### 3. Install Required Dependencies
Ensure all necessary packages are installed:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage & Pipeline Execution

To run the full end-to-end extraction, chunking, indexing, benchmarking, and query loop, execute:

```bash
python main.py
```

### What Happens During Execution:
1. **Extraction**: `DocumentExtractor` parses all documents from the `data/` folder.
2. **Chunking**: `EnterpriseChunker` splits content into overlapping semantic text blocks while attaching metadata payload structures.
3. **Indexing & Benchmarking**: `VectorStoreIndexer` populates ChromaDB in batches and reports batch execution time and throughput rates.
4. **Interactive CLI**: Prompts the user to enter natural language queries.

---

## 📊 Pipeline Validation & Output Benchmark

### 1. Ingestion & Benchmarking Statistics
```text
============================================================
🚀 INITIALIZING TASK 1: VECTOR ETL PIPELINE
============================================================

[1/3] Extracting legacy documents...
Extracted 50 source documents successfully.

[2/3] Performing semantic chunking & metadata enrichment...
Generated 290 semantic chunks with preserved attributes.

[3/3] Indexing into ChromaDB vector store with Cosine Index...
Successfully indexed 290 total chunks into ChromaDB vector store.
--------------------------------------------------
📊 BATCH INGESTION BENCHMARK RESULTS
  • Total Chunks Indexed: 290
  • Batch Execution Time: 19.7736 seconds
  • Ingestion Rate:       14.67 chunks/sec
--------------------------------------------------
```

### 2. Sample Runtime Test Queries

#### Test 1: PDF Policy Query
**Query**: `How many days of paid sick leave am I entitled to over a 3-year period?`  
**Result**:
```text
🔍 Results for: 'How many days of paid sick leave am I entitled to over a 3-year period?'

  [1] Source File: COMPANY POLICY MANUAL.pdf (Page/Row: 14)
      Cosine Distance Score: 0.2037 (Lower = Higher Similarity)
      Department: Executive | Tier: Tier-1
      Snippet: 6.5 SICK LEAVE
      You are entitled to 30 (thirty) days paid sick leave over a 3 (three) year period...
```

#### Test 2: Technical Markdown Query
**Query**: `How are microservices deployed in our cloud architecture?`  
**Result**:
```text
🔍 Results for: 'How are microservices deployed in our cloud architecture?'

  [1] Source File: engineering_arch.md (Page/Row: N/A)
      Cosine Distance Score: 0.4123 (Lower = Higher Similarity)
      Department: Engineering | Tier: Tier-1
      Snippet: All microservices deploy via Docker containers into secure client VPCs...
```

#### Test 3: Structured CSV Query
**Query**: `What is Bob Jones's role and email address?`  
**Result**:
```text
🔍 Results for: 'What is Bob Jones's role and email address?'

  [1] Source File: employee_directory.csv (Page/Row: N/A)
      Cosine Distance Score: 0.2932 (Lower = Higher Similarity)
      Department: Engineering | Tier: Tier-1
      Snippet: EmployeeID: 102, Name: Bob Jones, Role: Security Lead, Email: bob@client.com...
```

---

## 📷 Screenshots & Verification Outputs

All verification screenshot artifacts are categorized in the `Outputs/` directory:

- `Extracting_Semantic_Chunking_ChromaDB.png`: Verification of the full ETL run and benchmark logs.
- `PDF_testing _Output1.png`, `PDF_testing _Output2.png`, `PDF_testing _Output3.png`: Validation of PDF parsing and page-specific retrieval.
- `Markdown_Output1.png`, `Markdown_Output2.png`: Verification of technical Markdown documentation chunking and retrieval.
- `CSV_Output1.png`, `CSV_Output2.png`: Structured record retrieval validation from tabular data.

---

## 🔒 Security & RBAC Metadata Architecture

Every document chunk indexed into ChromaDB is tagged with mandatory metadata attributes:
- `department`: Business unit ownership (`Executive`, `Engineering`, `Finance`, etc.).
- `access_tier`: Security classification tier (`Tier-1`, `Tier-2`, `Tier-3`).
- `source`: Source file identifier.
- `page` / `row_index`: Precise origin location within source files.

These metadata tags enable downstream RAG components to enforce strict Role-Based Access Control (RBAC) metadata filtering on vector queries.