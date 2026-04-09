"""Send a test prompt to the Vacation Agent and display the response."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import VacationAgent

def main():
    print("=" * 60)
    print("  TEST PROMPT: 'I want a romantic beach getaway for 7 days'")
    print("=" * 60)
    print()

    agent = VacationAgent()
    print(f"Provider: {agent.provider} ({agent.model_name})")
    print(f"LLM Available: {agent.is_llm_available()}")
    print(f"Base URL: {agent.get_base_url()}")
    print()
    print("-" * 60)
    print("RESPONSE:")
    print("-" * 60)
    print()

    response = agent.chat("I want a romantic beach getaway for 7 days")
    print(response)

    print()
    print("-" * 60)

    # Check if we got a real LLM response or fallback
    if "[LLM Error" in response:
        print()
        print("  NOTE: LLM returned an error.")
        if "Cannot connect" in response:
            print("  FIX: Start Ollama with: ollama serve")
            print("       Then pull a model: ollama pull llama3")
        elif "HTTP" in response:
            print("  FIX: Check your API key is valid.")
        print()
        print("  The agent still works in fallback mode, but for")
        print("  full AI responses, configure an LLM provider.")
    else:
        print()
        print("  SUCCESS: Agent responded without errors!")

    print("=" * 60)

if __name__ == "__main__":
    main()
