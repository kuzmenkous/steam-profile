#!/bin/sh

# Define the application base directory
APP_DIR="/steam_profile_app/api"

# Wait for dependent services to be ready (PostgreSQL, Redis etc)
sleep 5

# Automatically load the appropriate .env file based on MODE
set -a
if [ "$MODE" = "DEV" ]; then
    ENV_FILE="$APP_DIR/.env.dev"
elif [ "$MODE" = "PROD" ]; then
    ENV_FILE="$APP_DIR/.env.prod"
fi

if [ -e "$ENV_FILE" ]; then
    # Load .env file safely, handling quotes and whitespace
    while IFS='=' read -r key value; do
        # Trim whitespace from the key and value
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)

        # Skip comments and empty lines
        case "$key" in
            \#* | "") continue ;;
        esac

        # Remove surrounding quotes from the value if present
        value=$(echo "$value" | sed 's/^["'\''"]//;s/["'\''"]$//')

        # Export the variable
        export "$key=$value"
    done < "$ENV_FILE"
    echo "Loaded environment file: $ENV_FILE"
else
    echo "No environment file found at $ENV_FILE. Exiting."
    exit 1
fi
set +a

# Navigate to the application directory
cd "$APP_DIR" || { echo "Failed to change directory to $APP_DIR. Exiting."; exit 1; }

# Check if STATIC_DIRECTORY is empty and default it to 'static' if it is
if [ -z "$STATIC_DIRECTORY" ]; then
    STATIC_DIRECTORY="static"
fi

echo "STATIC_DIRECTORY is set to: $STATIC_DIRECTORY"

# Check and create STATIC_DIRECTORY if necessary
if [ ! -d "$STATIC_DIRECTORY" ]; then
    echo "Creating directory $STATIC_DIRECTORY..."
    mkdir -p "$STATIC_DIRECTORY" || { echo "Failed to create directory $STATIC_DIRECTORY. Exiting."; exit 1; }
else
    echo "Directory $STATIC_DIRECTORY already exists."
fi

echo "TEMPLATES_DIRECTORY is set to: $TEMPLATES_DIRECTORY"

# Check and create TEMPLATES_DIRECTORY if necessary
if [ ! -d "$TEMPLATES_DIRECTORY" ]; then
    echo "Creating directory $TEMPLATES_DIRECTORY..."
    mkdir -p "$TEMPLATES_DIRECTORY" || { echo "Failed to create directory $TEMPLATES_DIRECTORY. Exiting."; exit 1; }
else
    echo "Directory $TEMPLATES_DIRECTORY already exists."
fi

# Database migration
if grep -qi '^ALEMBIC_RUN_MIGRATIONS=True' $ENV_FILE; then
    alembic upgrade head || { echo "Alembic upgrade failed. Exiting."; exit 1; }
fi

# Set the default message format for app mode
APP_MODE_MESSAGE="Starting the application in %s mode..."

# Check the MODE environment variable
if [ "$MODE" = "PROD" ]; then
    # Production mode: start Supervisor
    echo "Starting the application in production mode..."
    /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

elif [ "$MODE" = "DEV" ]; then
    # Development or debug mode
    # Check for debug mode in .env file
    if grep -qi '^APP_DEBUG=True' $ENV_FILE; then
        printf "$APP_MODE_MESSAGE" "debug"
        # Start FastAPI application with Uvicorn in development mode
        uvicorn src.main:app --reload --host 0.0.0.0 --port "$APP_PORT"
    else
        printf "$APP_MODE_MESSAGE" "production"
        # Start FastAPI application with Gunicorn in more stable development mode
        gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "0.0.0.0:$APP_PORT"
    fi
else
    echo "No valid MODE set. Exiting..."
    exit 1
fi