FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=fj2025.settings

WORKDIR /app

# System deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "fj2025.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]


