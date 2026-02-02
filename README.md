# Markdown Agent

Dual-distribution markdown quality validator with standalone script and MCP server modes.

## Quick Start

### Standalone Script (Copy to Any Project)

```bash
# Copy to project
cp markdown_validator.py /path/to/other-project/

# Run validation
python3 markdown_validator.py

# Auto-fix all issues
python3 markdown_validator.py --fix

# Check single file
python3 markdown_validator.py README.md --fix

# Get quality score
python3 markdown_validator.py . --score
```

### MCP Server (AI Tool Integration)

```bash
cd mcp-markdown-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add to MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json` or similar):

```json
{
  "mcpServers": {
    "markdown-quality": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-markdown-server/server.py"]
    }
  }
}
```

## Installation

### Prerequisites

```bash
# Install markdownlint-cli (required)
npm install -g markdownlint-cli
```

### Git Pre-Commit Hook

```bash
./setup-markdown-quality.sh
```

Validates markdown files before each commit. Bypass with `git commit --no-verify`.

## Use Cases

| Use Case | Best Solution |
|----------|--------------|
| This project with Copilot | Ask Copilot: `@workspace validate documentation` |
| Other Python projects | Copy `markdown_validator.py` standalone script |
| Other MCP projects | Setup `mcp-markdown-server/` and register |
| Any Git project | Install pre-commit hook with `setup-markdown-quality.sh` |
| CI/CD pipelines | Copy GitHub Action workflow |
| Real-time editing | Install VSCode markdownlint extension |

All solutions use the same `markdownlint-cli` engine for consistent quality standards.

## Configuration

Edit [.markdownlint.json](.markdownlint.json) to customize rules:

```json
{
  "MD013": { "line_length": 120 },
  "MD033": { "allowed_elements": ["details", "summary"] },
  "MD041": false
}
```

## Quality Scoring

- **100 points**: Perfect documentation
- **-2 points** per violation
- **Minimum**: 0 points

CI/CD enforces ≥80/100 threshold.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
