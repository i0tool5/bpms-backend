#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python -m daphne -b 0.0.0.0 bpms.asgi:application
