release: python manage.py migrate
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker DjangoCRM.asgi:application
