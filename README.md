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
1. Install Postgres
```bash
brew install postgresql@15
```

2. Start Postgres
```bash
brew services start postgresql@15
```

3. Install utilities
```bash
brew install libpq
```

Add to PATH
```bash
# ~/.zshrc
export PATH="/Applications/homebrew/opt/libpq/bin:$PATH"
```

Create role
```bash
createuser -s postgres
```

Create database
```bash
psql -U postgres
createdb lantern
```

### Start the service
```bash
gunicorn -c config/gunicorn/dev.py
```

### Kill the service
If you started the process in daemon mode, you can get the pid in the `.pid` file under `config/gunicorn`. Then run:
```bash
kill -9 <pid>
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

## Debugging Latency

1. Install Profiling packages

Make sure that you have the following Python packages installed:
```
django-extensions==3.2.3
snakeviz==2.2.0
```

2. Add debugging configuration in VSCode

In your `launch.json`, add the following configuration:
```
        {
            "name": "Lantern - Profile",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runprofileserver", "0.0.0.0:5000", "--use-cprofile", "--prof-path", "${workspaceFolder}/profile"
            ],
            "django": true,
            "justMyCode": true
        }
```

3. Add a `/profile` folder to your projects root directory if it doesn't already exist
4. Make queries as normal

The binary output to represent the profile of individual queries should be outputted to the `/profile` directory you've created

5. Open the profiler visualizer

From your terminal, run `snakeviz profile` in the root directory of the project.
