from typing import Any


def add_routes(app) -> None:
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
