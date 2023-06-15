# Lantern

Lantern is a Django application for managing application-level services for Khoj.

## Development
You should have Docker and Docker Compose installed on your system for quickest setup.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Build Docker Image
```bash
docker build -t lantern .
```

Docker Container
```bash
docker-compose up -d
```

### Enter Docker Container
```bash
docker exec -it lantern-web-1 bash
```

## Run migrations
```bash
python manage.py migrate
```
