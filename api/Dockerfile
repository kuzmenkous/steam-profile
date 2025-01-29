# Use Ubuntu 22.04 LTS as base image
FROM ubuntu:22.04

# Environment settings to avoid Python generating .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /steam_profile_app/api

# Install necessary packages and add the deadsnakes PPA for Python 3.13
RUN apt-get update && apt-get install -y \
    software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    supervisor \
    procps \
    cron \
    python3.13 \
    python3.13-venv \
    python3.13-gdbm \
    wget \
    gnupg \
    unzip \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.13
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python3.13

# Install Poetry
RUN pip install poetry

# Copy the Python dependencies file and install dependencies with Poetry
COPY pyproject.toml poetry.lock /steam_profile_app/api/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root -v \
    && rm -rf /root/.cache/pypoetry

# Copy the rest of the application
COPY . .

# Copy the supervisord configuration file
COPY ./supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make run script executable
COPY --chmod=765 scripts/run.sh /steam_profile_app/run.sh
RUN chmod +x /steam_profile_app/run.sh

CMD ["/steam_profile_app/run.sh"]