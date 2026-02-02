# Markdown Agent - AI Coding Instructions

## Project Overview

This is a **dual-distribution markdown quality validator** with two deployment modes:

1. **Standalone script** ([markdown_validator.py](../markdown_validator.py)) - portable, copy-to-any-project validator
2. **MCP server** ([mcp-markdown-server/](../mcp-markdown-server/)) - integrates with AI tools via Model Context Protocol

Both implementations wrap `markdownlint-cli` (Node.js) for consistent markdown validation across environments.

## Architecture Pattern

**Critical:** This project uses a "show, don't tell" README approach - the [README.md](../README.md) contains inline setup scripts and copy-paste commands, not prose explanations. When updating docs:

- Use code blocks with actual runnable commands
- Show complete file contents with heredoc syntax (`cat > file << 'EOF'`)
- Provide side-by-side comparison tables for different use cases

**Dependency boundary:** Python code calls external `markdownlint` CLI (Node.js) via subprocess, then parses JSON output. Never try to implement markdown validation in Python - always shell out to `markdownlint-cli`.

## Key Files

- [markdown_validator.py](../markdown_validator.py): Full standalone implementation with CLI (`--fix`, `--score` flags)
- [mcp-markdown-server/server.py](../mcp-markdown-server/server.py): MCP server with `check_markdown_file()` and `scan_project_docs()` tools
- [setup-markdown-quality.sh](../setup-markdown-quality.sh): Installs Git pre-commit hook for automatic validation
- [.markdownlint.json](../.markdownlint.json): Project-specific rules (120 char lines, HTML details allowed)
- [.github/workflows/markdown-quality.yml](../workflows/markdown-quality.yml): CI validation with 80/100 score threshold

## Development Workflows

### Testing the standalone script

```bash
python3 markdown_validator.py README.md --fix
python3 markdown_validator.py . --score
```

### Testing MCP server

```bash
cd mcp-markdown-server
source venv/bin/activate  # venv already exists
python server.py  # Runs FastMCP in stdio mode
```

### Setting up Git hooks

```bash
./setup-markdown-quality.sh  # Installs pre-commit validation
```

### CI/CD

GitHub Actions validates all markdown on push/PR, fails if quality score < 80/100.

## Code Patterns

### Subprocess invocation pattern

```python
result = subprocess.run(
    ["markdownlint", "--json", file_path],
    capture_output=True,
    text=True
)
violations = json.loads(result.stdout) if result.stdout else []
```

### arkdownlint Configuration

[.markdownlint.json](../.markdownlint.json) uses relaxed defaults:

- MD013: 120 character line limit (excludes code blocks/tables)
- MD033: Allows `<details>` and `<summary>` HTML tags
- MD041: Disabled (first line doesn't need to be H1)

**When modifying:** Test with `markdownlint --config .markdownlint.json README.md` before committing.

## MCP Server Status

**INCOMPLETE:** [mcp-markdown-server/server.py](../mcp-markdown-server/server.py) only has stub functions. To complete:

1. Copy validation logic from [markdown_validator.py](../markdown_validator.py) functions into MCP `@mcp.tool()` decorated functions
2. Keep function signatures matching the stubs (file_path, auto_fix, root_dir parameters)
3. Return structured dicts (not print statements) - FastMCP handles JSON serialization

## External Dependencies

- **markdownlint-cli** (Node.js): Must be installed globally (`npm install -g markdownlint-cli`)
- **FastMCP** (Python): Only for MCP server, not standalone script

**Error handling:** If `markdownlint` command not found, return `{"error": "markdownlint-cli not installed..."}` dict, don't raise exceptions.
