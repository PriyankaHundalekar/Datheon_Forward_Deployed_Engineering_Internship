# Enterprise AI System: End-to-End Multi-Task Engineering Series

An enterprise-grade AI solution featuring multi-document RAG with Role-Based Access Control (RBAC), multi-tenant security isolation, cross-encoder re-ranking, and an autonomous function-calling agent for ERP/CRM tool orchestration.

---

## 🗺️ Master Architecture Overview

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                            ENTERPRISE AI PLATFORM                           │
 └─────────────────────────────────────────────────────────────────────────────┘
                                       │
      ┌────────────────────────────────┼────────────────────────────────┐
      ▼                                ▼                                ▼
  [TASK 1]                         [TASK 2]                         [TASK 3]
  Multi-Document RAG               Multi-Tenant RBAC RAG            Autonomous Field Agent
  ├── Structured Data              ├── Department Isolation         ├── ReAct Engine (Ollama)
  ├── RBAC Security                ├── Query Expansion              ├── ERP/CRM API Wrappers
  └── Page Citations               └── Cross-Encoder Rerank         └── HITL Safety Loop
```

---

## 📂 Master Repository Directory Structure

```text
.
├── Task 1/                       # Multi-Document RAG Engine
│   ├── main.py                   # RAG pipeline CLI & document ingestor
│   ├── rbac.py                   # Role-Based Access Control matrix
│   ├── data/                     # Source documents & datasets
│   └── requirements.txt          # Python dependencies for Task 1
│
├── Task 2/                       # Secure Multi-Tenant RBAC RAG
│   ├── Outputs/                  # Screenshot evidence & verification logs
│   ├── main.py                   # Interactive multi-tenant CLI session
│   ├── query_rewriter.py         # LLM query expansion engine (Ollama qwen3:4b)
│   ├── rag_engine.py             # Secure vector engine & citation guardrails
│   ├── rbac.py                   # Department & clearance metadata filters
│   ├── reranker.py               # Cross-Encoder precision sorting
│   └── Sample_Testing_Questions.txt # Verified positive & negative test queries
│
├── Task 3/                       # Autonomous ERP/CRM Field Agent
│   ├── agent.py                  # ReAct (Thought-Action-Observation) loop
│   ├── mock_apis.py              # Mock ERP/CRM REST endpoints & live DBs
│   ├── tools.py                  # Tool definitions & sensitivity flags
│   └── main.py                   # Interactive CLI with Human-in-the-Loop approval
│
├── README.md                     # Comprehensive project documentation
└── requirements.txt              # Global environment dependencies
```

---

## 🛠️ Tech Stack & Frameworks

* **Local LLM Orchestration:** Ollama (`qwen3:4b`)
* **Vector Store & Embeddings:** ChromaDB
* **Re-Ranking Model:** HuggingFace `cross-encoder/ms-marco-MiniLM-L-6-v2`
* **Agentic Framework:** Custom ReAct (Thought-Action-Observation) Loop
* **API & Data Models:** Python 3.10+, Pydantic v2, FastAPI

---

## 🚀 Overview of Tasks & Implementation

### 🔹 Task 1: Enterprise Multi-Document RAG Pipeline
* **Core Objective:** Build a production-grade RAG pipeline ingesting diverse document formats (PDFs, Markdown, CSVs) with basic RBAC filtering.
* **Key Features:**
  * Multi-format ingestion and chunking.
  * Precise source page/row citation generation.
  * Role-based access control preventing unauthorized document access.

---

### 🔹 Task 2: Multi-Tenant RBAC RAG Engine with Re-Ranking & Guardrails
* **Core Objective:** Enforce strict departmental multi-tenancy, query re-writing, and cross-encoder re-ranking with strict hallucination guardrails.
* **Key Features:**
  * **Dynamic RBAC Metadata Filters:** Metadata isolation (`department == user_dept`) embedded directly into vector database queries.
  * **Query Expansion:** Local LLM query re-writing to expand sparse user prompts into dense search vectors.
  * **Cross-Encoder Re-Ranking:** Deep semantic scoring using `ms-marco-MiniLM-L-6-v2` to re-rank vector search results before LLM generation.
  * **Strict Hallucination Refusal:** Fails safely with clear refusal messages when documents are not accessible to the user.

---

### 🔹 Task 3: Autonomous Field Agent (ERP/CRM Tool Orchestration)
* **Core Objective:** Construct an autonomous tool-calling AI agent capable of executing transactional business operations against ERP and CRM systems.
* **Key Features:**
  * **ReAct Agent Loop:** Iterative `Thought` $\rightarrow$ `Action` $\rightarrow$ `Observation` execution cycle using local `qwen3:4b`.
  * **Mock REST Endpoints:** Inventory lookup (`ERP`), lead status update (`CRM`), and support ticket creation (`IT/Ops`).
  * **Human-in-the-Loop (HITL) Safety:** Sensitive write operations (modifying leads or creating tickets) automatically pause and require terminal confirmation (`[y/N]`) before hitting the endpoint.
  * **Validation & Error Recovery:** Catches invalid parameters or missing IDs and feeds structured error observations back to the LLM for self-correction.

---

## 🧪 Comprehensive Testing Guide

### 1️⃣ Testing Task 2 (Multi-Tenant RBAC RAG)
```bash
cd "Task 2"
python main.py
```
* **Positive Test (`alice_exec`):** 
  * Prompt: *"How many days of paid sick leave am I entitled to over a 3-year period?"*
  * Result: Success with page citations from `COMPANY POLICY MANUAL.pdf`.
* **Negative Test (`bob_eng`):** 
  * Prompt: *"How many days of paid sick leave am I entitled to over a 3-year period?"*
  * Result: Safe refusal due to department isolation (`Engineering` blocked from `Executive` docs).

---

### 2️⃣ Testing Task 3 (Autonomous ERP/CRM Field Agent)
```bash
cd "Task 3"
python main.py
```
* **Read Operation (Auto-executes without HITL):**
  ```text
  Check inventory stock level for product PRD-101.
  ```
* **Sensitive Write Operation (Triggers HITL Prompt):**
  ```text
  Update CRM lead LEAD-501 status to Qualified and assign to Alice.
  ```
* **Multi-Step ReAct Chain:**
  ```text
  Check stock for PRD-102. If stock is under 5 units, create a Critical IT ticket for Logistics.
  ```