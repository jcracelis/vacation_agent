#!/usr/bin/env python3
"""Python wrapper script for VS Code extension to call Vacation Agent."""

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


def handle_greeting():
    """Handle greeting command."""
    agent = VacationAgent()
    greeting = agent.greet()
    print(json.dumps({
        "success": True,
        "message": greeting
    }))


def handle_chat(message):
    """Handle chat message command."""
    agent = VacationAgent()
    response = agent.chat(message)
    print(json.dumps({
        "success": True,
        "message": response
    }))


def handle_plan_destination(args_json):
    """Handle destination planning command."""
    try:
        args = json.loads(args_json)
        agent = VacationAgent()
        result = agent.plan_destination(
            preference=args.get("preference", "beach"),
            duration_days=args.get("duration_days", 7),
            budget=args.get("budget", 2000),
            travelers=args.get("travelers", 2)
        )
        
        message = f"🏖️ **Destination Recommendation**\n\n"
        message += f"**{result.destination}, {result.country}**\n\n"
        message += f"{result.description}\n\n"
        message += f"**Estimated Cost:** ${result.estimated_cost:,.2f}\n"
        message += f"**Duration:** {result.duration_days} days\n"
        message += f"**Best Time to Visit:** {result.best_time_to_visit}\n\n"
        
        if result.highlights:
            message += "**Highlights:**\n"
            for highlight in result.highlights:
                message += f"• {highlight}\n"
        
        if result.tripadvisor_url:
            message += f"\n🔍 **Verified Source:** {result.tripadvisor_url}"
        
        print(json.dumps({
            "success": True,
            "message": message,
            "data": {
                "destination": result.destination,
                "country": result.country,
                "cost": result.estimated_cost
            }
        }))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": f"Error planning destination: {str(e)}"
        }))


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "message": "No command specified. Use: greet, chat, or plan_destination"
        }))
        sys.exit(1)

    command = sys.argv[1]

    if command == "greet":
        handle_greeting()
    elif command == "chat":
        if len(sys.argv) < 3:
            print(json.dumps({
                "success": False,
                "message": "No message provided"
            }))
            sys.exit(1)
        handle_chat(sys.argv[2])
    elif command == "plan_destination":
        if len(sys.argv) < 3:
            print(json.dumps({
                "success": False,
                "message": "No arguments provided"
            }))
            sys.exit(1)
        handle_plan_destination(sys.argv[2])
    else:
        print(json.dumps({
            "success": False,
            "message": f"Unknown command: {command}"
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
