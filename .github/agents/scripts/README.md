# Scripts

This directory contains utility scripts for development, testing, and deployment of the Vacation Agent.

## Available Scripts

**Note:** The primary helper scripts currently live in the parent `agents/` directory for easy access:

| Script | Location | Platform | Purpose |
|--------|----------|----------|---------|
| **validate.sh** | `../validate.sh` | Linux/WSL | 8-point code validation |
| **test_agent.bat** | `../test_agent.bat` | Windows | Full test suite runner |
| **setup-vscode-extension.sh** | `../setup-vscode-extension.sh` | Linux/WSL | Automated VS Code extension setup |

### Running Scripts

```bash
# Linux/WSL - Validation
bash ../validate.sh

# Windows - Tests
..\test_agent.bat

# Linux/WSL - Setup
bash ../setup-vscode-extension.sh
```

## Adding Scripts

When adding new scripts to this directory:

1. Place the script file here (e.g., `deploy.sh`)
2. Make it executable: `chmod +x script_name.sh`
3. Update this README with description and usage
4. Ensure the script has proper error handling

### Script Guidelines

- Include a header comment explaining purpose
- Add error handling and exit codes
- Support both success and failure cases
- Document usage in this README
- Avoid hardcoded paths - use variables or arguments

### Example Script Header

```bash
#!/bin/bash
# Script Name: deploy.sh
# Description: Deploy Vacation Agent to production
# Usage: bash deploy.sh [--dry-run]
# Platform: Linux/WSL

set -e  # Exit on error
```

## Script Categories

### Development
- Code formatting
- Linting
- Type checking
- Test runners

### Deployment
- Build scripts
- Package creation
- Environment setup

### Utilities
- Data migration
- Configuration generators
- Environment checkers

## Existing Scripts

_No additional scripts in this directory yet. Use the helper scripts in the parent directory._
