from typing import List, Optional

from domain.entities.user import User, Username, Password
from domain.repositories.user import UserRepository


class InMemoryUserRepository(UserRepository):

    def __init__(self) -> None:
        self.users: List[User] = []

    def all(self) -> List[User]:
        self.users = [User(username=Username("username"), password=Password("password"))]
        return self.users

    def find_by_username(self, username: str) -> Optional[User]:
        users_list = self.all()
        return next((user for user in users_list if username == user.username.value), None)


