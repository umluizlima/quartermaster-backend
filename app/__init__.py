import os

from flask import Flask


def create_app():
    """Create and configure the app."""
    app = Flask(__name__,
                instance_relative_config=True,
                static_url_path='')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'secret',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(app.instance_path, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize database
    from app.model import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.controller import (
        main, auth, user, category, thirdparty, item
    )
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(category.bp)
    app.register_blueprint(thirdparty.bp)
    app.register_blueprint(item.bp)

    return app
