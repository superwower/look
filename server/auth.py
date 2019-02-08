import boto3
import sys
from typing import List, Tuple, Iterator


def load_image(filename: str) -> bytes:
    with open(filename, 'rb') as image:
        return image.read()


class User:
    def __init__(self, display_name: str, username: str, password: str,
                 filename: str):
        self.display_name = display_name
        self.username = username
        self.password = password
        self.filename = filename


class UserRepository:
    def __init__(self) -> None:
        self.users: List[User] = [
            User("大月仁志", "otsuki.hitoshi", "password",
                 "images/otsuki.hitoshi.jpg"),
        ]

    def get_users(self) -> Iterator[User]:
        for user in self.users:
            yield user


class FaceAuthenticator:
    def __init__(self, user_repo: UserRepository) -> None:
        self.client = boto3.client('rekognition')
        self.user_repo = user_repo

    def auth(self, filename: str) -> Tuple[str, bool]:
        target_user_bytes = load_image(filename)
        for candidate_user in self.user_repo.get_users():
            candidate_user_bytes = load_image(candidate_user.filename)
            response = self.client.compare_faces(
                SourceImage={
                    'Bytes': candidate_user_bytes,
                },
                TargetImage={
                    'Bytes': target_user_bytes,
                },
                SimilarityThreshold=90)
            if len(response["FaceMatches"]) == 1:
                return (candidate_user.display_name, True)

        return ("", False)


def main() -> None:
    assert len(sys.argv) == 2
    # print(sys.argv[1])
    target_filename = sys.argv[1]
    user_repo = UserRepository()
    face_auth = FaceAuthenticator(user_repo)
    name, ok = face_auth.auth(target_filename)
    if ok:
        print(f"{name}として認証に成功しました")
    else:
        print(f"認証失敗")


if __name__ == "__main__":
    main()
