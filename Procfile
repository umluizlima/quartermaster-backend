web: echo $SECRET_KEY; flask db upgrade; gunicorn "app:create_app()" --log-file=-
