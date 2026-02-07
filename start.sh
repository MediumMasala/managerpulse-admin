#!/bin/bash
set -e

echo "=== Starting Django App ==="
echo "DATABASE_URL is: ${DATABASE_URL:0:50}..."
echo "DATABASE_PUBLIC_URL is: ${DATABASE_PUBLIC_URL:0:50}..."

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing anyway..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing..."

# Create superuser
echo "Creating superuser..."
python create_superuser.py || echo "Superuser creation skipped..."

# Start gunicorn
echo "Starting gunicorn on port $PORT..."
exec gunicorn admin_dashboard.wsgi --bind 0.0.0.0:$PORT
