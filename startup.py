#!/usr/bin/env python
"""Startup script that runs migrations and then starts the app."""
import os
import subprocess
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')

# Run migrations
print("=== Running migrations ===")
result = subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'])
print(f"Migration exit code: {result.returncode}")

# Collect static files
print("=== Collecting static files ===")
subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'])

# Create superuser if password is set
print("=== Creating superuser ===")
subprocess.run([sys.executable, 'create_superuser.py'])

# Start gunicorn
print("=== Starting gunicorn ===")
port = os.environ.get('PORT', '10000')
os.execvp('gunicorn', ['gunicorn', 'admin_dashboard.wsgi:application', '--bind', f'0.0.0.0:{port}'])
