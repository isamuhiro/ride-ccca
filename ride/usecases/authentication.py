from dataclasses import dataclass

from domain.entities.user import User
from domain.exceptions.user import UserNotFoundException, InvalidUserCredentialsException
from domain.repositories.user import UserRepository


@dataclass
class AuthenticateUser:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, user: User) -> bool:

        existing_user = self.user_repository.find_by_username(username=user.username.value)

        if not existing_user:
            raise UserNotFoundException

        if existing_user.password.value != user.password.value:
            raise InvalidUserCredentialsException

        return True
