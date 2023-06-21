# Lantern

Lantern is a Django application for managing application-level services for Khoj.

## Development
You should have Docker and Docker Compose installed on your system for quickest setup.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=True
```
### Database Setup
#### Install Postgres
```bash
brew install postgresql@15
```

#### Start Postgres
```bash
brew services start postgresql@15
```

#### Install utilities
```bash
brew install libpq
```

Add to PATH
```bash
# ~/.zshrc
export PATH="/Applications/homebrew/opt/libpq/bin:$PATH"
```

#### Create role
```bash
createuser -s postgres
```

### Start the service
```bash
python manage.py runserver 0.0.0.0:5000
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
