import os
from flask import Flask

from .model import db
from .route import add_routes


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(
            app.instance_path, 'look.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config_filename is not None:
        app.config.from_mapping(config_filename)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    add_routes(app)

    return app
