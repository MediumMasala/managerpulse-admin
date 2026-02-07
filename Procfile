web: python manage.py migrate && python manage.py collectstatic --noinput && python create_superuser.py && gunicorn admin_dashboard.wsgi --bind 0.0.0.0:$PORT
