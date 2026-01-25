#!/usr/bin/env bash
# Cleanup script to stop tracking virtualenv folders and commit .gitignore
# Run from the repo root: bash scripts/cleanup_venv.sh
set -euo pipefail

echo "Stopping tracking of common virtualenv folders (.venv, venv, env)"
# Unstage tracked venv folders if present
git rm -r --cached .venv || true
git rm -r --cached venv || true
git rm -r --cached env || true

# Ensure .gitignore exists
if [ ! -f .gitignore ]; then
  cat > .gitignore <<'EOF'
# Virtual environments
.venv/
venv/
env/
ENV/

# Python cache
__pycache__/
*.py[cod]
*.egg-info/

# OS
.DS_Store

# IDE
.vscode/
.idea/

# Dev artifacts
*.log

# Jupyter
.ipynb_checkpoints/

# Build
build/
dist/
EOF
  git add .gitignore
else
  git add .gitignore || true
fi

echo "Committing changes (unstage venv and add .gitignore)"
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "Stop tracking virtualenv; add .gitignore" || true
fi

echo "Done. Review status with 'git status'. To push run: git push origin HEAD"
