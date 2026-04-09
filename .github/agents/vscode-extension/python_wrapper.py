#!/usr/bin/env python3
"""Python wrapper script for VS Code extension to call Vacation Agent.

Supports multiple LLM providers:
- OpenAI (via OPENAI_API_KEY env var)
- Qwen (via QWEN_API_KEY env var)
"""

import sys
import os
import json
from pathlib import Path

# Add the project root to the path
# python_wrapper.py is at: .github/agents/vscode-extension/python_wrapper.py
# src/ is at: .github/agents/src/
# So we need to go up 2 levels (parent.parent)
project_root = Path(__file__).resolve().parent.parent
if not (project_root / "src" / "agent.py").exists():
    # Fallback: try going up 3 levels in case of different layout
    alt_root = Path(__file__).resolve().parent.parent.parent
    if (alt_root / "src" / "agent.py").exists():
        project_root = alt_root
sys.path.insert(0, str(project_root))

from src.agent import VacationAgent


def _get_api_keys():
    """Get API keys from environment."""
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "qwen_api_key": os.getenv("QWEN_API_KEY"),
    }


def _get_provider():
    """Determine which LLM provider to use based on available API keys."""
    # Prefer Qwen if both are available, otherwise use OpenAI
    if os.getenv("QWEN_API_KEY"):
        return "qwen"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return "openai"  # Default fallback


def handle_greeting():
    """Handle greeting command."""
    keys = _get_api_keys()
    provider = _get_provider()
    agent = VacationAgent(
        provider=provider,
        openai_api_key=keys["openai_api_key"],
        qwen_api_key=keys["qwen_api_key"],
    )
    greeting = agent.greet()
    print(json.dumps({
        "success": True,
        "message": greeting,
        "provider": agent.provider,
        "model": agent.model_name,
        "llm_available": agent.is_llm_available(),
    }))


def handle_chat(message):
    """Handle chat message command."""
    keys = _get_api_keys()
    provider = _get_provider()
    agent = VacationAgent(
        provider=provider,
        openai_api_key=keys["openai_api_key"],
        qwen_api_key=keys["qwen_api_key"],
    )
    response = agent.chat(message)
    print(json.dumps({
        "success": True,
        "message": response,
        "provider": agent.provider,
        "model": agent.model_name,
    }))


def handle_plan_destination(args_json):
    """Handle destination planning command."""
    try:
        args = json.loads(args_json)
        keys = _get_api_keys()
        provider = _get_provider()
        agent = VacationAgent(
            provider=provider,
            openai_api_key=keys["openai_api_key"],
            qwen_api_key=keys["qwen_api_key"],
        )
        result = agent.plan_destination(
            preference=args.get("preference", "beach"),
            duration_days=args.get("duration_days", 7),
            budget=args.get("budget", 2000),
            travelers=args.get("travelers", 2),
        )

        message = f"🏖️ **Destination Recommendation**\n\n"
        message += f"**{result.destination}, {result.country}**\n\n"
        message += f"{result.description}\n\n"
        message += f"**Estimated Cost:** ${result.estimated_cost:,.2f}\n"
        message += f"**Duration:** {result.duration_days} days\n"
        message += f"**Best Time to Visit:** {result.best_time_to_visit}\n"
        message += f"**LLM Provider:** {agent.provider} ({agent.model_name})\n\n"

        if result.highlights:
            message += "**Highlights:**\n"
            for highlight in result.highlights:
                message += f"• {highlight}\n"

        if result.tripadvisor_url:
            message += f"\n🔍 **Verified Source:** {result.tripadvisor_url}"

        print(json.dumps({
            "success": True,
            "message": message,
            "provider": agent.provider,
            "model": agent.model_name,
            "data": {
                "destination": result.destination,
                "country": result.country,
                "cost": result.estimated_cost,
            },
        }))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": f"Error planning destination: {str(e)}",
        }))


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "message": "No command specified. Use: greet, chat, or plan_destination",
        }))
        sys.exit(1)

    command = sys.argv[1]

    if command == "greet":
        handle_greeting()
    elif command == "chat":
        if len(sys.argv) < 3:
            print(json.dumps({
                "success": False,
                "message": "No message provided",
            }))
            sys.exit(1)
        handle_chat(sys.argv[2])
    elif command == "plan_destination":
        if len(sys.argv) < 3:
            print(json.dumps({
                "success": False,
                "message": "No arguments provided",
            }))
            sys.exit(1)
        handle_plan_destination(sys.argv[2])
    else:
        print(json.dumps({
            "success": False,
            "message": f"Unknown command: {command}",
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
