# Markdown Quality Validator

Dual-distribution Markdown quality validator and auto-fixer with standalone Python CLI (`markdown_validator.py`) and
Model Context Protocol (`mcp-markdown-server/server.py`) modes.

## Features & Quality Rules

| Rule ID & Name | Standard Enforced | Auto-Fix (`--fix` / `fix_markdown`) Behavior |
| --- | --- | --- |
| **`MD-SEP`**<br>Compact Separator | Always use compact `\| --- \|` separator cells with single-space margins. Never use `\| ------ \|` or `\| :--- \|`. | Rewrites all separator rows to `\| --- \|`. |
| **`MD-PAD`**<br>No Space-Padding | Never pad table cells with trailing spaces (`.ljust()`) to visually align vertical pipes (`\|`) across rows. | Strips multi-space cell padding to `\| cell \|`. |
| **`MD-COLS`**<br>Column Limit | Keep tables to `<= 5` columns in standard docs (`<= 3` columns in `--strict-3col` portrait print mode). | Stacks overflow columns vertically using `<br><strong>Header:</strong> Value`. |
| **`MD-TOKEN`**<br>Short Tokens & Basenames | Use short file basenames for links ([server.py](mcp-<wbr>markdown<wbr>-server/<wbr>server.py)) and unwrap multi-word prose backticks in table cells. | Shortens long link labels to basenames and unwraps multi-word prose backticks. |
| **`MD-WRAP`**<br>`<= 120`-Char Line Wrap | Wrap prose, list items, and blockquotes at `<= 120` chars (`MD013`), align list continuation indent (`MD007`), and keep blank lines around lists (`MD032`). | Wraps long lines cleanly without splitting `[label](url)` links or inline code spans. |

## Quick Start

### Standalone Script (Zero-Dependency Python 3)

```bash
# Copy to any project
cp markdown_validator.py /path/to/other-project/

# Run validation (default max 5 columns per table)
python3 markdown_validator.py .

# Auto-fix all compact table, padding, column width, and line-wrap issues
python3 markdown_validator.py . --fix

# Enforce strict 3-column portrait print mode
python3 markdown_validator.py . --strict-3col --fix

# Check single file
python3 markdown_validator.py README.md --fix

# Get repository quality score (0-100)
python3 markdown_validator.py . --score
```

### MCP Server (AI Tool Integration)

```bash
cd mcp-markdown-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add to your MCP configuration (`claude_desktop_config.json`, `.vscode/mcp.json`, or `mcp_config.json`):

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
# Optional: Install markdownlint-cli for external CLI hooks
npm install -g markdownlint-cli
```

### Git Pre-Commit Hook

```bash
./setup-markdown-quality.sh
```

Validates Markdown files before each commit. Bypass with `git commit --no-verify`.

## Use Cases

| Use Case | Recommended Solution |
| --- | --- |
| **GitHub Copilot / IDE Chat** | Ask Copilot: `@workspace validate documentation` |
| **Standalone Python Projects** | Copy `markdown_validator.py` and run `python3 markdown_validator.py . --fix` |
| **MCP-Enabled AI Assistants** | Register `mcp-markdown-server/server.py` (`validate_markdown`, `fix_markdown`, `validate_mermaid`, `check_links`) |
| **Git Pre-Commit Gate** | Install pre-commit hook with `./setup-markdown-quality.sh` |
| **CI/CD Pipelines** | Use [markdown-quality.yml](.github/workflows/markdown-quality.yml) |

## Configuration

Edit [.markdownlint.json](.markdownlint.json) to customize rules:

```json
{
  "MD013": { "line_length": 120 },
  "MD033": { "allowed_elements": ["details", "summary", "br", "wbr", "strong", "code", "sup", "sub"] },
  "MD041": false
}
```

## Quality Scoring

- **100 points**: Zero violations across all checked Markdown files
- **Deduction**: `-2` points per violation (minimum `0`)
- **CI Threshold**: `80/100` (configurable in workflow)

## License

MIT License - see [LICENSE](LICENSE) for details.
