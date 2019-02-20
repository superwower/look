from typing import Any
from flask import request, Flask
from flask import jsonify
import base64

from .face_search_service import FaceSearchService
from .attendance_service import (AbstractAttendanceService, AttendanceService,
                                 MockAttendanceService)
from .user_repo import UserRepository


def add_routes(app: Flask) -> None:
    @app.route('/api/auth', methods=['POST'])
    def authenticate() -> Any:
        collection_id = app.config.get("COLLECTION_ID")
        assert collection_id is not None
        face_search_service = FaceSearchService(collection_id)
        user_repo = UserRepository()
        attendance_service: AbstractAttendanceService
        endpoint = app.config.get("ATTENDANCE_SERVICE_ENDPOINT")
        if endpoint is not None:
            attendance_service = AttendanceService(endpoint)
        else:
            attendance_service = MockAttendanceService("http://endpont.hoge")

        raw_image = request.json.get("image")
        # mode: Optional[str] = request.json.get("mode")
        image = base64.b64decode(raw_image.split(",")[1])
        face_id, ok = face_search_service.search(image)
        if not ok:
            return jsonify(name="", error="Error in searching face")

        user, ok = user_repo.find_by_face_id(face_id)
        if not ok:
            return jsonify(name="", error="Failed to authenticate")

        if not attendance_service.submit(
                user):  # TODO: properly handle the request param
            return jsonify(name="", error="Failed to record attendance")

        return jsonify(name=user.email)
