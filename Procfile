web: gunicorn djecommerce.wsgi --log-file -
release: python manage.py migrate
python manage.py collectstatic