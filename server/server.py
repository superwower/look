from flask import Flask, request
import urllib
from typing import Any
from flask import jsonify
import base64

# from .auth import FaceAuthenticator, UserRepository

app = Flask(__name__)
# user_repo = UserRepository()
# face_auth = FaceAuthenticator(user_repo)


@app.route('/api/auth', methods=['POST'])  # type: ignore
def authenticate() -> Any:
    data = request.json["data"]
    image = base64.b64decode(data.split(",")[1])
    # username, ok = face_auth.auth(target_filename)

    # return {
    #     "username": username,
    #     "error": "" if ok else "Failed to authenticate"
    # }
    return jsonify(name="hoge@hoge.com")
