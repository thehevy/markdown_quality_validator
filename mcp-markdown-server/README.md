# Markdown Quality MCP Server

Model Context Protocol server for markdown validation and quality scoring.

## Installation

```bash
cd mcp-markdown-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Add to your MCP client config (e.g., Claude Desktop):

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

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

## Available Tools

### `check_markdown_file`

Check a single markdown file for quality issues.

**Parameters:**

- `file_path` (string): Path to markdown file
- `auto_fix` (bool, optional): Auto-fix violations if true

**Returns:**

```json
{
  "file": "README.md",
  "violations": 3,
  "details": [...],
  "quality_score": 94
}
```

### `scan_project_docs`

Scan all markdown files in a project directory.

**Parameters:**

- `root_dir` (string, default: "."): Root directory to scan

**Returns:**

```json
{
  "total_files": 5,
  "files_with_issues": 2,
  "total_violations": 8,
  "average_score": 92.0,
  "problem_files": [...]
}
```

## Testing

```bash
# Run in stdio mode (for testing)
source venv/bin/activate
python server.py

# Test with example prompt to AI:
# "Check the markdown quality of README.md"
```

## Dependencies

- `fastmcp>=2.14.0`: MCP server framework
- `markdownlint-cli`: Must be installed globally (`npm install -g markdownlint-cli`)
