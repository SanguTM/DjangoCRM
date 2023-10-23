release: python manage.py migrate
web: gunicorn DjangoCRM.asgi:application -k uvicorn.workers.UvicornWorker