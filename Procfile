web: daphne diplomski.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker vrticconnect.consumers.grupaConsumer -v2