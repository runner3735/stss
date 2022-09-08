
python manage.py collectstatic --noinput
gunicorn stss.wsgi:application --bind 0.0.0.0:8000

