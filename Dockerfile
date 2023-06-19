# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Set Environment Variables
RUN --mount=type=secret,id=DJANGO_SECRET_KEY \
  export DJANGO_SECRET_KEY=$(cat /run/secrets/DJANGO_SECRET_KEY) && \
  echo "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" > .env

RUN --mount=type=secret,id=POSTGRES_PASSWORD \
  export POSTGRES_PASSWORD=$(cat /run/secrets/POSTGRES_PASSWORD) && \
  echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env

# Copy project
COPY . .
RUN python manage.py collectstatic --noinput
