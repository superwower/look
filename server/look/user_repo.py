from typing import List, Iterator, Optional


class User:
    def __init__(self, username: str, password: str, filename: str):
        self.username = username
        self.password = password
        self.filename = filename


class UserRepository:
    def __init__(self) -> None:
        self.users: List[User] = []
        pass

    def get_users(self) -> Iterator[User]:
        for user in self.users:
            yield user

    def find_by_face_id(self, face_id: str) -> Optional[User]:
        # TODO: run query
        users: List[User] = []
        assert len(users) <= 1, f"mutiple users with face_id {face_id}"

        return None if len(users) == 0 else users[0]
