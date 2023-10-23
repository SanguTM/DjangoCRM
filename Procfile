web: gunicorn -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:8080" --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate