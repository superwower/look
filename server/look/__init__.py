import os
from flask import Flask
from typing import Optional

from .model import db
from .route import add_routes


def create_app(config_filename: Optional[str] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(  # type: ignore
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(
            app.instance_path, 'look.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if config_filename is not None:
        _, ext = os.path.splitext(config_filename)
        assert ext == ".cfg"
        app.config.from_pyfile(config_filename)  # type: ignore

    db.init_app(app)
    add_routes(app)

    return app
