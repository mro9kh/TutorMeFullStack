release: python manage.py migrate
web: python manage.py migrate && python manage.py collectstatic && gunicorn locallibrary.wsgi