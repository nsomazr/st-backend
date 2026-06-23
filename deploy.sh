#!/usr/bin/env bash
# Production deploy — Gunicorn via PM2
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PM2_APP_NAME="${PM2_APP_NAME:-st-backend}"

echo "==> Smart Travels Backend — PM2 deploy"

if ! command -v pm2 &>/dev/null; then
  echo "Error: pm2 is not installed. Run: npm install -g pm2"
  exit 1
fi

if [[ ! -f .env ]]; then
  echo "Error: .env not found. Copy .env.example to .env and configure production values."
  exit 1
fi

# Load PORT and other vars from .env
set -a
# shellcheck disable=SC1091
source .env
set +a

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

echo "Collecting static files..."
python manage.py collectstatic --noinput

if ! python manage.py shell -c "from services.models import Service; exit(0 if Service.objects.exists() else 1)" 2>/dev/null; then
  echo "Seeding default services..."
  python manage.py seed_services
fi

export PM2_APP_NAME

if pm2 describe "$PM2_APP_NAME" &>/dev/null; then
  echo "Restarting PM2 app: $PM2_APP_NAME"
  pm2 restart ecosystem.config.cjs --env production --update-env
else
  echo "Starting PM2 app: $PM2_APP_NAME"
  pm2 start ecosystem.config.cjs --env production
fi

pm2 save

echo ""
echo "✅ Backend deployed with PM2"
echo "   App name : $PM2_APP_NAME"
echo "   Port     : ${PORT:-8094}"
echo "   Logs     : pm2 logs $PM2_APP_NAME"
echo "   Status   : pm2 status $PM2_APP_NAME"
