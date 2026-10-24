# Task 3: Autonomous Field Agent – Enterprise ERP/CRM Tool Orchestration

An autonomous function-calling AI agent that interfaces directly with mock enterprise ERP and CRM REST endpoints. The agent executes business operations through dynamic ReAct (Thought-Action-Observation) cycles, enforces input validation loops, handles errors gracefully, and enforces strict Human-in-the-Loop (HITL) confirmation before executing sensitive write operations.

---

## 🏗️ Architectural Workflow Diagram

```text
  [User Task Prompt]
         │
         ▼
  AutonomousFieldAgent (agent.py) ──► Re-Act Reasoning Loop (Ollama qwen3:4b)
         │
         ▼
  Tool Dispatcher (tools.py) ──► Validates Schema & Identifies Sensitivity
         │
         ├──► [Read Operation] ──► Auto-Executes Mock API (mock_apis.py)
         │
         └──► [Write Operation] ──► Triggers HITL Prompt ([y/N] Approval)
                                          │
                                          ▼ (If Approved)
                                     Executes REST Endpoint & Mutates DB
                                          │
                                          ▼
                                     Feeds Observation back to Agent Loop
```

---

## 📂 Project Directory Structure (`Task 3/`)

```text
Task 3/
├── mock_apis.py         # Mock ERP/CRM REST endpoints & stateful databases
├── tools.py             # Schema-validated tool definitions & sensitivity flags
├── agent.py             # ReAct agent loop managing thought-action-observation cycles
├── main.py              # Interactive terminal CLI with HITL approval callbacks
├── README.md            # Task 3 project documentation & architecture guide
└── requirements.txt     # Python package dependencies
```

---

## 🚀 Key Features & Implementation Modules

1. **Mock Enterprise Endpoints (`mock_apis.py`)**:
   * Simulates stateful database records for ERP inventory lookups, CRM lead status updates, and IT support ticket generation.

2. **Structured Tool Schemas (`tools.py`)**:
   * Wraps API functions into standardized JSON schemas and classifies actions as read-only or sensitive writes (`is_sensitive: True`).

3. **ReAct Autonomous Agent (`agent.py`)**:
   * Leverages local Ollama (`qwen3:4b`) to run iterative reasoning cycles, parsing actions and feeding tool observations back into the context.

4. **Human-in-the-Loop (HITL) Safety (`main.py`)**:
   * Automatically intercepts sensitive modifications (e.g., updating leads, creating tickets) and prompts the supervisor for explicit terminal confirmation (`[y/N]`).

5. **Validation & Error Loops**:
   * Rejects malformed arguments or invalid statuses and feeds structured error observations back to the LLM for self-correction.

---

## 🔒 Execution & Testing Guide

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Autonomous Agent CLI:**
   ```bash
   python main.py
   ```

3. **Sample Test Prompts:**
   * **Read Operation (Auto-executes without HITL):**
     ```text
     Check inventory stock level for product PRD-101.
     ```
   * **Write Operation (Triggers HITL prompt):**
     ```text
     Update CRM lead LEAD-501 status to Qualified and assign to Alice.
     ```
   * **Multi-Step ReAct Chain:**
     ```text
     Check stock for PRD-102. If stock is low, create a Critical IT ticket for Logistics.
     ```