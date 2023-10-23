release: python manage.py migrate
web: uvicorn src.main:app --host=0.0.0.0 --port=${PORT:-5000}
worker: python manage.py runworker channel_layer -v2