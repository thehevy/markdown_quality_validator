from fastmcp import FastMCP
import subprocess
import json
from pathlib import Path
from typing import Dict, List

mcp = FastMCP("Markdown Quality Server")

def calculate_quality_score(violations: List) -> int:
    """Returns 0-100 quality score."""
    if not violations:
        return 100
    score = 100 - (len(violations) * 2)
    return max(0, score)

@mcp.tool()
def check_markdown_file(file_path: str, auto_fix: bool = False) -> Dict:
    """Check markdown file quality and optionally fix issues."""
    violations = []
    
    # Run markdownlint
    try:
        result = subprocess.run(
            ["markdownlint", "--json", file_path],
            capture_output=True,
            text=True
        )
        if result.stdout:
            violations = json.loads(result.stdout)
    except FileNotFoundError:
        return {"error": "markdownlint-cli not installed. Run: npm install -g markdownlint-cli"}
    except Exception as e:
        return {"error": str(e)}
    
    if auto_fix and violations:
        # Auto-fix using markdownlint --fix
        subprocess.run(["markdownlint", "--fix", file_path], check=False)
        
        # Re-check
        result = subprocess.run(
            ["markdownlint", "--json", file_path],
            capture_output=True,
            text=True
        )
        new_violations = json.loads(result.stdout) if result.stdout else []
        fixed_count = len(violations) - len(new_violations)
        
        return {
            "file": file_path,
            "original_violations": len(violations),
            "remaining_violations": len(new_violations),
            "fixes_applied": fixed_count,
            "quality_score": calculate_quality_score(new_violations)
        }
    
    return {
        "file": file_path,
        "violations": len(violations),
        "details": violations[:10],
        "quality_score": calculate_quality_score(violations)
    }

@mcp.tool()
def scan_project_docs(root_dir: str = ".") -> Dict:
    """Scan all markdown files in project."""
    markdown_files = list(Path(root_dir).rglob("*.md"))
    
    # Exclude common ignored directories
    excluded = {'.git', 'node_modules', 'venv', '.venv', 'dist', 'build'}
    markdown_files = [
        f for f in markdown_files 
        if not any(part.startswith('.') or part in excluded for part in f.parts)
    ]
    
    results = []
    total_violations = 0
    
    for md_file in markdown_files:
        result = check_markdown_file(str(md_file), auto_fix=False)
        if 'violations' in result and result['violations'] > 0:
            total_violations += result['violations']
            results.append({
                "file": str(md_file),
                "violations": result['violations'],
                "score": result['quality_score']
            })
    
    avg_score = sum(r['score'] for r in results) / len(results) if results else 100
    
    return {
        "total_files": len(markdown_files),
        "files_with_issues": len(results),
        "total_violations": total_violations,
        "average_score": round(avg_score, 1),
        "problem_files": sorted(results, key=lambda x: x['violations'], reverse=True)[:10]
    }

if __name__ == "__main__":
    mcp.run()
