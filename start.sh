#!/usr/bin/env bash
# Local development — Django runserver (not PM2)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${PORT:-8000}"

echo "==> Smart Travels Backend — development start"

if [[ ! -f .env ]]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
  echo "⚠️  Edit .env with your settings before continuing."
fi

if [[ ! -d venv ]]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

if ! python manage.py shell -c "from services.models import Service; exit(0 if Service.objects.exists() else 1)" 2>/dev/null; then
  echo "Seeding default services..."
  python manage.py seed_services
fi

echo "Starting Django dev server on http://localhost:${PORT}"
python manage.py runserver "0.0.0.0:${PORT}"
