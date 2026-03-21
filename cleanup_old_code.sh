#!/bin/bash
# cleanup_old_code.sh - Safely delete old root-level code files
# This script will backup old files before deletion

echo "🧹 Therapeutic AI Chatbot - Old Code Cleanup"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: This script must be run from the project root directory"
    echo "Current path: $(pwd)"
    exit 1
fi

echo "📂 About to backup and delete old files:"
echo ""

# Files to backup
FILES_TO_REMOVE=(
    "behaviour.py"
    "llm.py"
    "main.py"
    "modes.py"
    "prompts.py"
    "safety.py"
    "schemas.py"
)

# Count existing files
count=0
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo "  - $file"
        ((count++))
    fi
done

if [ $count -eq 0 ]; then
    echo "✅ No old files found - already clean!"
    exit 0
fi

echo ""
echo "Found $count old files to remove"
echo ""

# Ask for confirmation
read -p "Create backup folder and move files? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
fi

# Create backup folder
BACKUP_DIR="old_code_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📦 Created backup folder: $BACKUP_DIR"
echo ""

# Move files
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        mv "$file" "$BACKUP_DIR/"
        echo "✓ Moved $file → $BACKUP_DIR/"
    fi
done

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Next steps:"
echo "1. Run tests: pytest"
echo "2. Test imports: python -c \"from app.main import app; print('✓ OK')\""
echo "3. Start server: uvicorn app.main:app --reload"
echo "4. Delete backup: rm -rf $BACKUP_DIR/"
echo ""
