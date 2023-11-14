from pydantic import BaseModel

from domain.entities.user import User, Username, Password


class UserLogin(BaseModel):
    username: str
    password: str

    def to_user(self) -> User:
        return User(Username(self.username), Password(self.password))
