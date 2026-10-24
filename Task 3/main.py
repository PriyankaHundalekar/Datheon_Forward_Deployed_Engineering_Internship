import sys
from agent import AutonomousFieldAgent

def hitl_confirmation_callback(tool_name: str, kwargs: dict) -> bool:
    """Human-in-the-Loop confirmation prompt for sensitive write operations[cite: 2]."""
    print("\n" + "!" * 70)
    print("⚠️  HUMAN-IN-THE-LOOP APPROVAL REQUIRED FOR SENSITIVE TRANSACTION")
    print(f"   • Action Requested: {tool_name}")
    print(f"   • Arguments: {kwargs}")
    print("!" * 70)
    
    choice = input("👉 Do you approve executing this enterprise write operation? [y/N]: ").strip().lower()
    return choice == 'y'

def main():
    print("=" * 70)
    print("🤖 TASK 3: AUTONOMOUS FIELD AGENT (ERP/CRM ORCHESTRATOR)")
    print("=" * 70)
    
    agent = AutonomousFieldAgent(model_name="qwen3:4b", hitl_callback=hitl_confirmation_callback)
    
    print("\nSample Prompts to Test:")
    print("1. Read Operation (No HITL): 'Check the inventory stock level for product PRD-101.'")
    print("2. Write Operation (Requires HITL): 'Update lead LEAD-501 status to Qualified and assign to Bob.'")
    print("3. Multi-step Operation: 'Check stock for PRD-102. If stock is low, create a Critical IT ticket for Logistics.'")
    print("=" * 70)

    while True:
        try:
            prompt = input("\n💬 Enter task for agent (or 'exit' to quit): ").strip()
            if not prompt or prompt.lower() == 'exit':
                print("Exiting Task 3 Agent. Goodbye!")
                break
            
            final_res = agent.run(prompt)
            print(f"\n✅ [TASK COMPLETED]:\n{final_res}")
            print("-" * 70)
            
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

if __name__ == "__main__":
    main()