import os
from rag_engine import EnterpriseRAGEngine

def main():
    print("=" * 60)
    print("🔐 INITIALIZING TASK 2: ENTERPRISE MULTI-TENANT RBAC RAG")
    print("=" * 60)
    
    # Initialize Engine (points to Task 1 vector database)
    engine = EnterpriseRAGEngine(persist_dir="../Task 1/chroma_db", collection_name="enterprise_docs")
    
    print("\nAvailable Test User Profiles for RBAC Demo:")
    print("  1. alice_exec    (Executive Department, Tier-1 Clearance)")
    print("  2. bob_eng       (Engineering Department, Tier-1 Clearance)")
    print("  3. charlie_guest (Engineering Department, Tier-3 Clearance)")
    
    username = input("\n👤 Enter username profile to log in as (default: alice_exec): ").strip()
    if not username:
        username = "alice_exec"
        
    print(f"\n✅ Logged in successfully as profile: {username}")
    print("🤖 ENTERPRISE SECURE RAG SYSTEM (Type 'exit' to quit)")
    print("-" * 60)
    
    while True:
        try:
            query = input(f"\n💬 [{username}] Enter your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session. Goodbye!")
            break
            
        if not query:
            continue
        if query.lower() == 'exit':
            print("Exiting session. Goodbye!")
            break
            
        print("\n🔄 Processing query (Rewriting -> RBAC Filtering -> Retrieving -> Re-ranking -> Guardrail Gen)...")
        result = engine.query(query, username)
        
        print(f"\n🔍 Expanded Query: {result.get('expanded_query', query)}")
        print(f"\n💡 Answer:\n{result['answer']}")
        print("\n📚 Verifiable Citations:")
        for citation in result.get('citations', []):
            print(f"  • {citation}")
        print("-" * 60)

if __name__ == "__main__":
    main()