#!/bin/bash

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate

echo "Starting web server..."
gunicorn --workers=3 stss.wsgi:application --bind 0.0.0.0:8000
