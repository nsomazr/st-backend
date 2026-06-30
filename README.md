# Smart Travels by HL — Backend

Django REST API for the Smart Travels travel booking system.

## Prerequisites

- Python 3.12+
- Docker & Docker Compose (for MySQL)
- Virtual environment (recommended)

## Quick Start

### 1. Start MySQL

```bash
docker compose up -d mysql
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your settings (especially SECRET_KEY and MAIL credentials)
```

### 3. Install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
python manage.py seed_services
python manage.py create_admin
```

Default admin login: `admin` / `admin123` (override with `--username` and `--password`).

### 5. Start development server

```bash
./start.sh
# or manually:
python manage.py runserver
```

API available at `http://localhost:8094/api/`

## PM2 Production Deploy

Prerequisites: `npm install -g pm2`, MySQL running, `.env` configured for production.

```bash
cp .env.example .env
# Edit .env: DEBUG=False, SECRET_KEY, DB credentials, MAIL credentials

chmod +x deploy.sh start.sh
./deploy.sh
```

This will:
1. Install Python dependencies in `venv/`
2. Run migrations and collect static files
3. Start/restart Gunicorn via PM2 (`st-backend` by default)

**PM2 commands:**
```bash
pm2 status st-backend
pm2 logs st-backend
pm2 restart st-backend
pm2 stop st-backend
```

**Environment variables** (in `.env`):
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8094` | Gunicorn bind port |
| `GUNICORN_WORKERS` | `3` | Worker processes |
| `PM2_APP_NAME` | `st-backend` | PM2 process name |
| `ADMIN_ALERT_EMAIL` | `info@akisgroup.net` | Admin email for new bookings |
| `ADMIN_ALERT_PHONES` | `+255713689686,+255757113006` | Comma-separated admin SMS numbers |
| `BEEM_SMS_API_KEY` | — | Beem Africa SMS API key |
| `BEEM_SMS_SECRET_KEY` | — | Beem Africa SMS secret |
| `BEEM_SMS_SOURCE_ADDR` | `SMARTTRAV` | Approved Beem sender ID |

When a customer books, the admin receives:
- **Email** at `ADMIN_ALERT_EMAIL` with full booking details
- **SMS** to each number in `ADMIN_ALERT_PHONES` via Beem Africa

## Docker (full stack)

```bash
cp .env.example .env
docker compose up --build
```

## API Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/bookings/create/` | Public |
| GET | `/api/bookings/` | Admin JWT |
| GET | `/api/bookings/<ref>/` | Public/Admin |
| PATCH | `/api/bookings/<ref>/status/` | Admin JWT |
| GET | `/api/services/` | Public |
| POST | `/api/contact/` | Public |
| POST | `/api/admin/login/` | Public |
| GET | `/api/admin/dashboard/stats/` | Admin JWT |

## Production

- Set `DEBUG=False` and a strong `SECRET_KEY`
- `ALLOWED_HOSTS=api.smarttravel.co.tz`
- `CORS_ALLOWED_ORIGINS=https://smarttravel.co.tz`
- Run with Gunicorn behind a reverse proxy
