#!/usr/bin/env python3
"""Python wrapper script for VS Code extension to call Vacation Agent.

Supported LLM providers (auto-detected by available credentials):
- Ollama  — local, no API key needed (OLLAMA_BASE_URL env var)
- Qwen    — Alibaba Cloud DashScope (QWEN_API_KEY env var)
- OpenAI  — GPT models (OPENAI_API_KEY env var)

Usage:
    python python_wrapper.py greet
    python python_wrapper.py chat "I want a beach vacation"
    python python_wrapper.py plan_destination '{"preference":"beach","duration_days":7,"budget":3000}'
"""

import sys
import os
import json
from pathlib import Path

# ─── Path Resolution ────────────────────────────────────────────────────────
# python_wrapper.py lives at: .github/agents/vscode-extension/python_wrapper.py
# src/ lives at:              .github/agents/src/
# → Need to go up 2 levels from this file
_project_root = Path(__file__).resolve().parent.parent
if not (_project_root / "src" / "agent.py").exists():
    _alt_root = Path(__file__).resolve().parent.parent.parent
    if (_alt_root / "src" / "agent.py").exists():
        _project_root = _alt_root
sys.path.insert(0, str(_project_root))

from src.agent import VacationAgent


# ─── Credential Helpers ─────────────────────────────────────────────────────


def _load_credentials() -> dict:
    """Read all LLM credentials from environment variables.

    Returns:
        Dict with openai_api_key, qwen_api_key, ollama_base_url
    """
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "qwen_api_key": os.getenv("QWEN_API_KEY"),
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL"),
    }


# ─── Command Handlers ───────────────────────────────────────────────────────


def _make_agent() -> VacationAgent:
    """Factory: create a VacationAgent with current environment credentials."""
    creds = _load_credentials()
    return VacationAgent(**creds)


def _output(success: bool, message: str, **extra):
    """Print a JSON response to stdout.

    Args:
        success: Whether the operation succeeded
        message: Human-readable response text
        **extra: Additional fields to include in the JSON
    """
    payload = {"success": success, "message": message}
    payload.update(extra)
    print(json.dumps(payload))


def handle_greeting():
    """Handle greeting command."""
    agent = _make_agent()
    greeting = agent.greet()
    _output(
        True,
        greeting,
        provider=agent.provider,
        model=agent.model_name,
        llm_available=agent.is_llm_available(),
    )


def handle_chat(message: str):
    """Handle chat message command.

    Args:
        message: User's chat message text
    """
    agent = _make_agent()
    response = agent.chat(message)
    _output(
        True,
        response,
        provider=agent.provider,
        model=agent.model_name,
    )


def handle_plan_destination(args_json: str):
    """Handle destination planning command.

    Args:
        args_json: JSON string with preference, duration_days, budget, travelers
    """
    try:
        args = json.loads(args_json)
        agent = _make_agent()
        result = agent.plan_destination(
            preference=args.get("preference", "beach"),
            duration_days=args.get("duration_days", 7),
            budget=args.get("budget", 2000),
            travelers=args.get("travelers", 2),
        )

        message = (
            f"🏖️ **Destination Recommendation**\n\n"
            f"**{result.destination}, {result.country}**\n\n"
            f"{result.description}\n\n"
            f"**Estimated Cost:** ${result.estimated_cost:,.2f}\n"
            f"**Duration:** {result.duration_days} days\n"
            f"**Best Time to Visit:** {result.best_time_to_visit}\n"
            f"**LLM Provider:** {agent.provider} ({agent.model_name})\n\n"
        )

        if result.highlights:
            message += "**Highlights:**\n"
            for highlight in result.highlights:
                message += f"• {highlight}\n"

        if result.tripadvisor_url:
            message += f"\n🔍 **Verified Source:** {result.tripadvisor_url}"

        _output(
            True,
            message,
            provider=agent.provider,
            model=agent.model_name,
            data={
                "destination": result.destination,
                "country": result.country,
                "cost": result.estimated_cost,
            },
        )
    except Exception as e:
        _output(False, f"Error planning destination: {str(e)}")


# ─── Main Entry Point ───────────────────────────────────────────────────────


_COMMANDS = {
    "greet": (1, handle_greeting),
    "chat": (2, handle_chat),
    "plan_destination": (2, handle_plan_destination),
}


def main():
    """Parse CLI arguments and dispatch to the appropriate handler."""
    if len(sys.argv) < 2:
        _output(False, "No command specified. Use: greet, chat, or plan_destination")
        sys.exit(1)

    command = sys.argv[1]

    if command not in _COMMANDS:
        _output(False, f"Unknown command: {command}")
        sys.exit(1)

    min_args, handler = _COMMANDS[command]
    if len(sys.argv) < min_args + 1:
        _output(False, f"Missing arguments for '{command}'")
        sys.exit(1)

    # Handlers that take extra args receive sys.argv[2]
    if min_args == 1:
        handler()
    else:
        handler(sys.argv[2])


if __name__ == "__main__":
    main()
