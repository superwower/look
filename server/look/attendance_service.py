import requests
from requests_ntlm import HttpNtlmAuth
from enum import Enum
from typing import NamedTuple
import os
from abc import ABC, abstractmethod


class UserAuthInfo(NamedTuple):
    email: str
    password: str


class AttendanceMode(Enum):
    START = "01"
    FINISH = "02"


class AbstractAttendanceService(ABC):
    @abstractmethod
    def ping(self, user: UserAuthInfo) -> str:
        pass

    @abstractmethod
    def submit(self,
               user: UserAuthInfo,
               mode: AttendanceMode = AttendanceMode.START) -> bool:
        pass


class MockAttendanceService(AbstractAttendanceService):
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def ping(self, user: UserAuthInfo) -> str:
        return "Pong"

    def submit(self,
               user: UserAuthInfo,
               mode: AttendanceMode = AttendanceMode.START) -> bool:
        return True


class AttendanceService(AbstractAttendanceService):
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def ping(self, user: UserAuthInfo) -> str:
        r = requests.get(
            self.endpoint,
            auth=HttpNtlmAuth(user.email, user.password),
            verify=False)

        r.raise_for_status()
        if r.status_code == requests.codes.ok:
            return "Pong"

        return ""

    def submit(self,
               user: UserAuthInfo,
               mode: AttendanceMode = AttendanceMode.START) -> bool:
        # First login and get cookies
        session = requests.Session()
        session.get(
            self.endpoint,
            auth=HttpNtlmAuth(user.email, user.password),
            verify=False)

        # use the cookies above to post attendance
        payload = {"SubmitMode": str(mode)}
        r = session.post(self.endpoint, data=payload, verify=False)

        r.raise_for_status()

        if r.status_code == requests.codes.ok:
            print(r.text)
            return True

        return False


if __name__ == "__main__":
    user = UserAuthInfo(os.environ['LOOK_USERNAME'],
                        os.environ['LOOK_PASSWORD'])
    service = AttendanceService(endpoint=os.environ['LOOK_ENDPOINT'])
    print(service.submit(user))
