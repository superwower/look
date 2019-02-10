import requests
from requests_ntlm import HttpNtlmAuth
from enum import Enum
import toml
from typing import NamedTuple


class UserAuthInfo(NamedTuple):
    username: str
    password: str


class AttendanceMode(Enum):
    START = "01"
    FINISH = "02"


class MockAttendanceService:
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def ping(self, user: UserAuthInfo) -> str:
        return "Pong"

    def submit(self,
               user: UserAuthInfo,
               mode: AttendanceMode = AttendanceMode.START) -> bool:
        return True


class AttendanceService:
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def ping(self, user: UserAuthInfo) -> str:
        r = requests.get(
            self.endpoint,
            auth=HttpNtlmAuth(user.username, user.password),
            verify=False)

        r.raise_for_status()
        if r.status_code == requests.codes.ok:
            return "Pong"

        return ""

    def submit(self,
               user: UserAuthInfo,
               mode: AttendanceMode = AttendanceMode.START) -> bool:
        payload = {"SubmitMode": mode}
        r = requests.post(
            self.endpoint,
            data=payload,
            auth=HttpNtlmAuth(user.username, user.password),
            verify=False)

        r.raise_for_status()

        if r.status_code == requests.codes.ok:
            print(r.text)
            return True

        return False


if __name__ == "__main__":
    with open("./config.toml", "r") as f:
        config = toml.load(f)

    user = UserAuthInfo(config["user"]["username"], config["user"]["password"])
    service = AttendanceService(endpoint=config["endpoint"])
    print(service.ping(user))
