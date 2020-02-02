import os
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_url_path=''
    )

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'secret',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(app.instance_path, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)

    from flask_sslify import SSLify
    if 'DYNO' in os.environ:  # only trigger SSLify if app is running on Heroku
        sslify = SSLify(app)

    from app.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from app.cli import create_admin
    app.cli.add_command(create_admin)

    from app.api import api
    app.register_blueprint(api)

    return app
