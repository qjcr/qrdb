#!/bin/bash -e
pyenv global 3.9.5
. ~/rooms/venv/bin/activate
pyenv exec python manage.py migrate
yes yes | pyenv exec python manage.py collectstatic
pyenv exec gunicorn qrdb.wsgi -b unix:/societies/qjcr/rooms/web.sock #0.0.0.0:6969
