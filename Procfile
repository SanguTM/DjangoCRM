release: python manage.py migrate
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
worker: python manage.py runworker channel_layer -v2