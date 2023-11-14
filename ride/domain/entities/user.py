import hashlib
from dataclasses import dataclass, field

from domain.exceptions.user import PasswordLengthException, UsernameLengthException


@dataclass
class Password:
    value: str

    def __init__(self, value: str):
        if len(value) <= 4:
            raise PasswordLengthException()

        self.value = value


@dataclass
class Username:
    value: str

    def __init__(self, value: str):
        if len(value) < 4:
            raise UsernameLengthException()

        self.value = value


@dataclass
class User:
    username: Username
    password: Password
    _hashed_password: str = field(init=False, repr=False, default='')

    def __post_init__(self) -> None:
        self.hash_password()

    def hashed_password(self) -> str:
        return self._hashed_password

    def hash_password(self) -> None:
        sha1 = hashlib.sha1()
        sha1.update(self.password.value.encode('utf-8'))
        self._hashed_password = sha1.hexdigest()

    def validate_password(self, password: str) -> bool:
        return password == self.password.value
