# Contributing to Markdown Agent

Thank you for considering contributing to Markdown Agent! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.12+
- Node.js 20+ (for markdownlint-cli)
- Git

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/thehevy/markdown_quality_validator.git
cd markdown_quality_validator

# Install Node.js dependencies
npm install -g markdownlint-cli

# Set up MCP server development environment
cd mcp-markdown-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install pre-commit hook
./setup-markdown-quality.sh
```

## Code Structure

- `markdown_validator.py` - Standalone script with full validation logic
- `mcp-markdown-server/server.py` - FastMCP server implementation
- `.markdownlint.json` - Markdown linting rules
- `setup-markdown-quality.sh` - Git hook installer
- `.github/workflows/` - CI/CD pipelines

## Development Workflow

### Testing Changes

```bash
# Test standalone validator
python3 markdown_validator.py . --fix

# Test MCP server
cd mcp-markdown-server
source venv/bin/activate
python server.py  # Run in stdio mode
```

### Code Style

- **Python**: Follow PEP 8 conventions
- **Line length**: 120 characters max
- **Type hints**: Use for function parameters and returns
- **Documentation**: Update README.md and inline docstrings

### Testing Markdown Quality

All markdown files must pass validation before committing:

```bash
# Check all markdown
python3 markdown_validator.py .

# Auto-fix issues
python3 markdown_validator.py . --fix

# Check quality score (must be ≥80)
python3 markdown_validator.py . --score
```

## Making Changes

### Bug Fixes

1. Create an issue describing the bug
2. Fork the repository
3. Create a branch: `git checkout -b fix/issue-description`
4. Make your changes
5. Test thoroughly
6. Commit with clear messages
7. Submit a pull request

### New Features

1. Open an issue to discuss the feature first
2. Follow the same fork/branch workflow
3. Update documentation
4. Add tests if applicable
5. Ensure CI passes

### Documentation Updates

- Update README.md for user-facing changes
- Update mcp-markdown-server/README.md for MCP-specific changes
- Update .github/copilot-instructions.md for AI agent guidance
- Ensure all markdown passes quality checks

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
✅ Good:
- "Fix quality score calculation for empty violations"
- "Add support for custom markdownlint configs"
- "Update README with MCP server examples"

❌ Bad:
- "fix bug"
- "update code"
- "changes"
```

## Pull Request Process

1. Ensure your code passes all quality checks
2. Update documentation as needed
3. Reference related issues in PR description
4. Wait for CI/CD to pass
5. Address review feedback promptly

## Code Review Standards

- All code must have clear purpose and documentation
- No breaking changes without discussion
- Maintain backward compatibility when possible
- Follow existing patterns and conventions

## Questions or Issues?

- Open a GitHub issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive in discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
