# Task 2: Enterprise Multi-Tenant RAG with Role-Based Access Control (RBAC)

A secure, production-grade Retrieval-Augmented Generation (RAG) architecture that enforces strict departmental multi-tenancy, transforms raw search queries, leverages cross-encoder re-ranking for maximum relevance precision, and integrates strict hallucination guardrails with verifiable source page citations.

---

## 🏗️ Architectural Workflow Diagram

```text
  [User Query & Login Profile]
               │
               ▼
    RBACManager (rbac.py) ──► Enforces Department Metadata Filters
               │
               ▼
    QueryRewriter (query_rewriter.py) ──► Expands Query via Local Ollama (qwen3:4b)
               │
               ▼
    Vector Store Retrieval (ChromaDB) ──► Filters by Security Clearance
               │
               ▼
    CrossEncoderReranker (reranker.py) ──► Re-ranks top chunks (ms-marco-MiniLM-L-6-v2)
               │
               ▼
    EnterpriseRAGEngine (rag_engine.py) ──► Generates Guardrailed Response + Page Citations
```

---

## 📂 Project Directory Structure (`Task 2/`)

```text
Task 2/
├── Outputs/                 # Validation screenshots & test evidence
│   ├── Authorized Access_Bob1.png
│   ├── Authorized Access_Bob2.png
│   └── Restricted Access_Bob.png
│
├── venv/                    # Virtual environment
├── .gitignore               # Git ignore configuration
├── main.py                  # Orchestration script & interactive multi-tenant CLI
├── query_rewriter.py        # LLM query expansion module (Ollama qwen3:4b)
├── rag_engine.py            # Core secure RAG pipeline with citation guardrails
├── rbac.py                  # User security profiles & metadata isolation filters
├── README.md                # Task 2 project documentation & architecture guide
├── requirements.txt         # Python package dependencies
└── Sample_Testing_Questions.txt # Positive & negative test case references
```

---

## 🚀 Key Features & Implementation Modules

1. **Role-Based Access Control (`rbac.py`)**:
   * Defines user clearance profiles (`alice_exec`, `bob_eng`, `charlie_guest`) across departments (Executive, Engineering) and access tiers.
   * Constructs secure metadata filters injected directly into vector store lookups to prevent cross-department data leakage.

2. **Query Re-Writing (`query_rewriter.py`)**:
   * Utilizes local Ollama (`qwen3:4b`) to transform conversational, brief user prompts into dense, information-rich search queries optimized for vector recall.

3. **Cross-Encoder Re-Ranking (`reranker.py`)**:
   * Employs `cross-encoder/ms-marco-MiniLM-L-6-v2` to deeply evaluate query-document pair relevance, sorting retrieved candidates to ensure highest-precision context selection.

4. **Secure RAG & Citation Guardrails (`rag_engine.py`)**:
   * Enforces strict local LLM generation constraints: refuses to fabricate answers when context is missing, and explicitly extracts verifiable source file names and page/row numbers.

5. **Interactive Multi-Tenant CLI (`main.py`)**:
   * Simulates multi-user enterprise login sessions to test positive authorization and negative RBAC security isolation in real time.

---

## 🔒 Security & Testing Matrix

| User Profile | Department | Clearance | Tested Query | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **`alice_exec`** | Executive | Tier-1 | *"How many days of paid sick leave..."* | **Success**: Returns policy details with page citations. |
| **`bob_eng`** | Engineering | Tier-1 | *"How many days of paid sick leave..."* | **Refusal**: Blocked by RBAC; safe guardrail fallback triggered. |
| **`bob_eng`** | Engineering | Tier-1 | *"What are the core details of our architecture?"* | **Success**: Returns engineering documentation securely. |

---

## ⚙️ Getting Started & Execution

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Local Ollama Server is Running:**
   Verify `qwen3:4b` is accessible locally via Ollama.

3. **Run the Secure Multi-Tenant RAG CLI:**
   ```bash
   python main.py
   ```