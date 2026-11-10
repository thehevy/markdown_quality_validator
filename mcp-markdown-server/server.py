#!/usr/bin/env python3
"""
MCP Server exposing validate_markdown, fix_markdown, validate_mermaid, check_links,
check_markdown_file, and scan_project_docs backed by markdown_validator.py.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from markdown_validator import (
    check_markdown_quality,
    check_relative_links,
    validate_all_documentation,
    validate_and_fix_markdown_text,
    validate_mermaid_blocks,
)

try:
    from fastmcp import FastMCP
    mcp = FastMCP("Markdown Quality Server")
except ImportError:
    mcp = None


def validate_markdown(file_path: str = "", markdown_text: str = "", max_cols: int = 5) -> Dict[str, Any]:
    """Validate Markdown file or inline text against compact '| --- |' table and line-wrapping rules."""
    if file_path:
        return check_markdown_quality(file_path, auto_fix=False, max_cols=max_cols)
    _, issues = validate_and_fix_markdown_text(markdown_text, auto_fix=False, max_cols=max_cols)
    return {"valid": len(issues) == 0, "issue_count": len(issues), "issues": issues}


def fix_markdown(file_path: str = "", markdown_text: str = "", max_cols: int = 5) -> Dict[str, Any]:
    """Auto-fix Markdown tables to compact '| --- |' separators, strip cell padding, and wrap long lines."""
    if file_path:
        return check_markdown_quality(file_path, auto_fix=True, max_cols=max_cols)
    fixed, remaining = validate_and_fix_markdown_text(markdown_text, auto_fix=True, max_cols=max_cols)
    return {
        "valid": len(remaining) == 0,
        "fixed_markdown": fixed,
        "remaining_issue_count": len(remaining),
        "remaining_issues": remaining,
    }


def validate_mermaid(file_path: str = "", markdown_text: str = "") -> Dict[str, Any]:
    """Validate Mermaid fenced code blocks in a file or inline Markdown string."""
    txt = Path(file_path).read_text(encoding="utf-8", errors="ignore") if file_path else markdown_text
    return validate_mermaid_blocks(txt)


def check_links(file_path: str) -> Dict[str, Any]:
    """Verify all relative and file:/// links in a Markdown file resolve on disk."""
    return check_relative_links(Path(file_path))


if mcp is not None:
    mcp.tool()(validate_markdown)
    mcp.tool()(fix_markdown)
    mcp.tool()(validate_mermaid)
    mcp.tool()(check_links)

    @mcp.tool()
    def check_markdown_file(file_path: str, auto_fix: bool = False, max_cols: int = 5) -> Dict[str, Any]:
        """Backward-compatible tool: check or auto-fix a Markdown file."""
        return check_markdown_quality(file_path, auto_fix=auto_fix, max_cols=max_cols)

    @mcp.tool()
    def scan_project_docs(root_dir: str = ".", auto_fix: bool = False, max_cols: int = 5) -> Dict[str, Any]:
        """Backward-compatible tool: scan all Markdown files in a project."""
        return validate_all_documentation(root_dir, auto_fix=auto_fix, max_cols=max_cols)


if __name__ == "__main__":
    if mcp is not None:
        mcp.run()
