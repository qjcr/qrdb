pyenv global 3.9.5
. ~/rooms/venv/bin/activate
pyenv exec python manage.py runserver
pyenv exec gunicorn qrdb.wsgi -b unix:/societies/qjcr/rooms/web.sock #0.0.0.0:6969
