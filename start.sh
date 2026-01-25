
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"


if [ ! -d ".venv" ]; then
  echo "Creating virtual environment at .venv..."
  python3 -m venv .venv
fi

. .venv/bin/activate

pip install --upgrade pip
if ! pip install -r requirements.txt; then
  echo "Initial install failed. Attempting fallback for torch (CPU wheel) and required packages..."
  pip install --index-url https://download.pytorch.org/whl/cpu torch || true
  pip install -r requirements.txt --no-deps || true
  pip install sentence-transformers transformers pandas numpy requests beautifulsoup4 geopy || true
fi

echo "Starting Flask app (port 5001)..."
python app.py
