#!/bin/bash
# setup-markdown-quality.sh
# Install pre-commit hook for markdown validation

set -e

HOOK_PATH=".git/hooks/pre-commit"

# Check if markdownlint-cli is installed
if ! command -v markdownlint &> /dev/null; then
    echo "⚠️  markdownlint-cli not found. Installing..."
    npm install -g markdownlint-cli
fi

# Create pre-commit hook
cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash
# Pre-commit hook: Validate markdown quality

# Get staged markdown files
STAGED_MD=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$' || true)

if [ -z "$STAGED_MD" ]; then
    exit 0
fi

echo "🔍 Checking markdown quality..."

# Run validator on staged files
for file in $STAGED_MD; do
    python3 markdown_validator.py "$file"
    if [ $? -ne 0 ]; then
        echo "❌ Markdown quality issues found in $file"
        echo "💡 Run: python3 markdown_validator.py $file --fix"
        exit 1
    fi
done

echo "✅ All markdown files pass quality checks"
exit 0
EOF

chmod +x "$HOOK_PATH"

echo "✅ Pre-commit hook installed at $HOOK_PATH"
echo "📝 Markdown files will be validated before each commit"
echo ""
echo "To test: git commit (with staged .md files)"
echo "To bypass: git commit --no-verify"
