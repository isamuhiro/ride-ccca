import pytest

from domain.entities.user import User, Username, Password
from domain.exceptions.user import UserNotFoundException, InvalidUserCredentialsException
from infra.repositories.user import InMemoryUserRepository
from usecases.authentication import AuthenticateUser


def test_should_authenticate_user() -> None:
    authenticate_user = AuthenticateUser(user_repository=InMemoryUserRepository())
    output = authenticate_user.execute(User(Username("username"), Password("password")))
    assert output is True


def test_should_raise_user_not_found() -> None:
    authenticate_user = AuthenticateUser(user_repository=InMemoryUserRepository())
    with pytest.raises(UserNotFoundException) as exc:
        authenticate_user.execute(User(Username("user"), Password("password")))
        assert exc.errisinstance(UserNotFoundException) is True


def test_should_raise_invalid_user_credentials() -> None:
    authenticate_user = AuthenticateUser(user_repository=InMemoryUserRepository())
    with pytest.raises(InvalidUserCredentialsException) as exc:
        authenticate_user.execute(User(Username("username"), Password("invalid password")))
        assert exc.errisinstance(InvalidUserCredentialsException) is True
