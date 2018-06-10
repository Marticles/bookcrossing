from app import create_app
application = create_app()

#gunicorn -k gevent -c gun.conf wsgi:application