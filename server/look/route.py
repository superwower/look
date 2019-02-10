from typing import Any, Optional
from flask import request
from flask import jsonify
import base64

from .face_search_service import FaceSearchService
from .attendance_service import MockAttendanceService
from .user_repo import UserRepository


def add_routes(app) -> None:
    @app.route('/api/auth', methods=['POST'])  # type: ignore
    def authenticate() -> Any:
        collection_id = "look"
        # app.config["COLLECTION_ID"]
        face_search_service = FaceSearchService(collection_id)
        user_repo = UserRepository()
        # TODO: replace with a real one
        attendance_service = MockAttendanceService("http://endpont.hoge")
        raw_image = request.json.get("data")
        mode: Optional[str] = request.json.get("mode")
        image = base64.b64decode(raw_image.split(",")[1])
        face_id, ok = face_search_service.search(image)
        if not ok:
            return jsonify(name="", error="Error in searching face")

        user = user_repo.find_by_face_id(face_id)
        if user is None:
            return jsonify(name="", error="Failed to authenticate")

        if not attendance_service.submit(user, mode):
            return jsonify(name="", error="Failed to record attendance")

        return jsonify(name=user.email)
