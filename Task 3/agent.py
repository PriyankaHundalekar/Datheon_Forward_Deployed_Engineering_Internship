import json
import ollama
from tools import TOOLS_SCHEMA, execute_tool

SYSTEM_PROMPT = """You are an Autonomous Field Agent for enterprise ERP/CRM tool orchestration.
You solve tasks step-by-step using a ReAct (Thought-Action-Observation) loop.

Available Tools:
1. lookup_inventory(product_id: str) - Read ERP inventory stock.
2. update_lead_status(lead_id: str, new_status: str, assigned_owner: str) - Update CRM lead.
3. create_support_ticket(title: str, priority: str, department: str, description: str) - Create support ticket.

FORMAT INSTRUCTIONS:
To call a tool, format your output strictly as:
Thought: <Your reasoning about what step to take next>
Action: <tool_name>
Action Input: <JSON formatted string of arguments>

When you have the final answer or completed all operations, output:
Thought: I have completed the task.
Final Answer: <Your comprehensive explanation to the user>

Rules:
- Never guess arguments. If an API returns an error, modify your input or ask for clarification.
- Always execute step-by-step.
"""

class AutonomousFieldAgent:
    """Autonomous ReAct agent displaying Thought-Action-Observation cycles."""

    def __init__(self, model_name: str = "qwen3:4b", hitl_callback=None):
        self.model_name = model_name
        self.hitl_callback = hitl_callback  # Human-in-the-loop approval callback function
        self.tools_lookup = {t["name"]: t for t in TOOLS_SCHEMA}

    def run(self, user_prompt: str, max_steps: int = 5) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User Request: {user_prompt}"}
        ]

        print(f"\n🎯 [AGENT TASK INITIATED]: {user_prompt}")
        print("=" * 70)

        for step in range(1, max_steps + 1):
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                options={"temperature": 0.1}
            )

            assistant_output = response["message"]["content"].strip()
            print(f"\n🤖 [STEP {step}] Output:\n{assistant_output}")

            # Check if task finished
            if "Final Answer:" in assistant_output:
                final_answer = assistant_output.split("Final Answer:")[-1].strip()
                return final_answer

            # Parse Action and Action Input
            if "Action:" in assistant_output and "Action Input:" in assistant_output:
                try:
                    action_line = [line for line in assistant_output.split("\n") if line.startswith("Action:")][0]
                    tool_name = action_line.replace("Action:", "").strip()

                    input_block = assistant_output.split("Action Input:")[-1].strip()
                    # Extract JSON object
                    json_start = input_block.find("{")
                    json_end = input_block.rfind("}") + 1
                    kwargs = json.loads(input_block[json_start:json_end])

                    tool_meta = self.tools_lookup.get(tool_name, {})
                    is_sensitive = tool_meta.get("is_sensitive", False)

                    # --- Human-in-the-Loop (HITL) Check ---
                    if is_sensitive and self.hitl_callback:
                        approved = self.hitl_callback(tool_name, kwargs)
                        if not approved:
                            observation = "Observation: Human supervisor REJECTED this sensitive write operation. Task aborted by user."
                            print(f"\n⛔ {observation}")
                            messages.append({"role": "assistant", "content": assistant_output})
                            messages.append({"role": "user", "content": observation})
                            continue

                    # Execute Tool
                    tool_result = execute_tool(tool_name, kwargs)
                    observation = f"Observation: {json.dumps(tool_result)}"
                    print(f"\n👁️ [OBSERVATION]: {observation}")

                    # Feed observation back to agent loop
                    messages.append({"role": "assistant", "content": assistant_output})
                    messages.append({"role": "user", "content": observation})

                except Exception as e:
                    error_obs = f"Observation: Error parsing action input or executing tool ({e}). Please fix JSON input format."
                    print(f"\n⚠️ {error_obs}")
                    messages.append({"role": "assistant", "content": assistant_output})
                    messages.append({"role": "user", "content": error_obs})
            else:
                messages.append({"role": "assistant", "content": assistant_output})
                messages.append({"role": "user", "content": "Please continue by outputting Thought and Action or Final Answer."})

        return "Agent reached maximum step limit before completing task."