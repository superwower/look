from flask import Flask, request
import urllib

from .auth import FaceAuthenticator, UserRepository

app = Flask(__name__)
# user_repo = UserRepository()
# face_auth = FaceAuthenticator(user_repo)


@app.route('/api/auth', methods=['POST'])
def authenticate():
    # url_encoded = request.args.get('company-data')
    # url_decoded = urllib.unquote(url_encoded).decode('utf8')
    # company_data = json.loads(url_decoded)
    # print(company_data)
    # username, ok = face_auth.auth(target_filename)

    return {
        "username": username,
        "error": "" if ok else "Failed to authenticate"
    }
