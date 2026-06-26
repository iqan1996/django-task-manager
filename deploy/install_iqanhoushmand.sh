#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=/home/iqan/Django_Course
SERVICE_NAME=django-course
DOMAIN=iqanhoushmand.ir

cd "$PROJECT_DIR"

. "$PROJECT_DIR/venv/bin/activate"
python -m pip install -r requirements.txt
python manage.py migrate --noinput
DJANGO_DEBUG=False python manage.py collectstatic --noinput

SECRET_KEY="$(python - <<'PY'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
PY
)"

sudo cp "$PROJECT_DIR/deploy/django-course.service" "/etc/systemd/system/$SERVICE_NAME.service"
sudo env SECRET_KEY="$SECRET_KEY" python - <<'PY'
from pathlib import Path
import os

path = Path("/etc/systemd/system/django-course.service")
text = path.read_text()
text = text.replace(
    "DJANGO_SECRET_KEY=change-me-before-start",
    f"DJANGO_SECRET_KEY={os.environ['SECRET_KEY']}",
)
path.write_text(text)
PY

sudo cp "$PROJECT_DIR/deploy/iqanhoushmand.ir.nginx" "/etc/nginx/sites-available/$DOMAIN"
sudo ln -sfn "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"

sudo systemctl daemon-reload
sudo systemctl enable --now "$SERVICE_NAME"
sudo nginx -t
sudo systemctl reload nginx

systemctl --no-pager --full status "$SERVICE_NAME"
