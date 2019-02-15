from typing import Any, Optional
from flask import request
from flask import jsonify
import base64

from .face_search_service import FaceSearchService
from .attendance_service import AttendanceService, MockAttendanceService, AttendanceMode
from .user_repo import UserRepository


def add_routes(app) -> None:
    @app.route('/api/auth', methods=['POST'])  # type: ignore
    def authenticate() -> Any:
        collection_id = app.config.get("collection_id")
        assert collection_id is not None
        collection_id = "look"
        face_search_service = FaceSearchService(collection_id)
        user_repo = UserRepository()
        if app.config.get("attendance_service_type") == "real":
            endpoint = app.config.get("attendance_service_endpoint") 
            assert endpoint is not None
            attendance_service = AttendanceService(endpoint)
        else:
            attendance_service = MockAttendanceService("http://endpont.hoge")
        raw_image = request.json.get("image")
        mode: Optional[str] = request.json.get("mode")
        image = base64.b64decode(raw_image.split(",")[1])
        face_id, ok = face_search_service.search(image)
        if not ok:
            return jsonify(name="", error="Error in searching face")

        user = user_repo.find_by_face_id(face_id)
        if user is None:
            return jsonify(name="", error="Failed to authenticate")

        if not attendance_service.submit(user, mode=None):  # TODO: properly handle the request param
            return jsonify(name="", error="Failed to record attendance")

        return jsonify(name=user.email)
