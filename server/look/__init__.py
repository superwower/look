import os
from flask import Flask, request
from typing import Any, Optional
from flask import jsonify
import base64

from .face_search_service import FaceSearchService
from .attendance_service import AttendanceService
from .user_repo import UserRepository
from .model import db


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(app.instance_path, 'look.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config_filename is not None:
        app.config.from_mapping(config_filename)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app) 

    @app.route('/api/auth', methods=['POST'])  # type: ignore
    def authenticate() -> Any:
        collectionId = "FIXME"  # FIXME: fix here
        face_search_service = FaceSearchService(collectionId)
        user_repo = UserRepository()
        attendance_service = AttendanceService()
        raw_image = request.json.get("data")
        mode: Optional[str] = request.json.get("mode")
        image = base64.b64decode(raw_image.split(",")[1])
        face_id, ok = face_search_service.search(image)
        if not ok:
            return jsonify(name="", error="Error in searching face")
    
        user = user_repo.find_by_face_id(face_id)
        if attendance_service.submit(user, mode):
            return jsonify(name=user.username)

        return jsonify(name="", error="")

    return app
