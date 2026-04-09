# Contributing to Vacation Agent

Thank you for your interest in contributing to Vacation Agent! This guide will help you get started.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributions from everyone.

## How to Contribute

### 1. Fork the Repository

Click "Fork" on GitHub to create your copy.

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

**Branch naming conventions:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions

### 3. Make Your Changes

Follow the coding standards below.

### 4. Validate Your Changes

Before submitting, run the validation script:

```bash
# Linux/WSL
bash validate.sh

# Windows
test_agent.bat
```

Ensure all checks pass.

### 5. Commit Your Changes

Use descriptive commit messages:

```bash
git commit -m "feat: add budget validation for trip planning

- Add cost validation in agent.py
- Update tests for budget function
- Update README with new feature"
```

**Commit message format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation change
- `style:` - Code formatting
- `refactor:` - Code restructuring
- `test:` - Test addition/update
- `chore:` - Maintenance task

### 6. Push and Open a Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a PR on GitHub with:
- Clear description of changes
- Link to related issues (if any)
- Screenshots for UI changes

---

## Python Contribution Guidelines

### Code Style

- Follow **PEP 8** guidelines
- Use **Black** for formatting: `black src/`
- Use **type hints** for all function signatures
- Keep functions under 50 lines when possible

### Linting

```bash
# Check style
flake8 src/ tests/

# Type checking
mypy src/

# Format code
black src/ tests/
```

### Writing Tests

- All new features require tests
- Aim for **>80% code coverage**
- Use descriptive test names: `test_validate_source_approves_tripadvisor()`
- Test both success and failure cases

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
```

### Docstrings

Use Google-style docstrings for all public functions:

```python
def function_name(param1: str, param2: int) -> dict:
    """One-line summary.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this error occurs
    """
```

---

## TypeScript/VS Code Extension Guidelines

### Code Style

- Use **ESLint** for linting: `npm run lint`
- Follow **TypeScript strict mode**
- Use **interfaces** for object shapes
- Prefer `const` over `let` when possible

### Compilation

Always compile before submitting:

```bash
cd vscode-extension
npm run compile
```

### Webview Development

- Test the chat interface in the Extension Development Host (F5)
- Verify message formatting works correctly
- Test error handling and edge cases

### Linting

```bash
npm run lint
```

---

## Documentation Guidelines

### README Updates

Any feature change that affects user experience **must** update:
- Root `README.md` (if applicable)
- `.github/agents/README.md`
- `.github/agents/vscode-extension/README.md` (for extension changes)

### Documentation Standards

- Use **Markdown** format
- Include code examples with syntax highlighting
- Provide platform-specific instructions (Windows, Linux, Mac) when relevant
- Keep instructions concise but complete
- Use tables for configuration options

### Empty Directories

The following directories have placeholder READMEs:
- `docs/` - Add actual documentation files here
- `notebooks/` - Add Jupyter notebooks for exploratory work
- `scripts/` - Add utility scripts here

If you add files to these directories, update their READMEs accordingly.

---

## Pull Request Checklist

Before submitting your PR, verify:

- [ ] All tests pass: `pytest tests/`
- [ ] Code is formatted: `black src/ tests/`
- [ ] Linting passes: `flake8 src/` and `mypy src/`
- [ ] TypeScript compiles: `npm run compile` (in vscode-extension/)
- [ ] Validation script passes: `bash validate.sh` or `test_agent.bat`
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No secrets or API keys in code
- [ ] `.gitignore` is respected

---

## Review Process

1. A maintainer will review your PR within 1-2 weeks
2. Address any requested changes
3. Once approved, your PR will be merged

---

## Reporting Issues

Use GitHub Issues to report:
- 🐛 **Bugs** - Include steps to reproduce, expected/actual behavior, and environment details
- 💡 **Feature Requests** - Describe the problem your feature solves
- 📖 **Documentation** - Suggest improvements or report inaccuracies

---

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🌴
