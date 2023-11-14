from http import HTTPStatus
from typing import Union, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from domain.exceptions.user import (UserNotFoundException,
                                    InvalidUserCredentialsException,
                                    PasswordLengthException,
                                    UsernameLengthException)
from infra.models.user import UserLogin
from infra.repositories.user import InMemoryUserRepository
from usecases.authentication import AuthenticateUser

import re

app = FastAPI()


class SmokeResponse(BaseModel):
    is_ok: bool


@app.get("/smoke")
async def root() -> dict[str, bool]:
    return {"is_ok": True}


auth_responses: dict[Union[int, str], dict[str, Any]] = {
    HTTPStatus.OK.value: {"description": "User successfully logged in"},
    HTTPStatus.NOT_FOUND.value: {
        "description": "User Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "User not found"}
            }
        }
    },
    HTTPStatus.UNAUTHORIZED.value: {
        "description": "Invalid User Credentials",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid user credentials"}
            }
        }
    }
}


@app.post("/auth", responses=auth_responses)
async def auth(user_login: UserLogin) -> bool:
    try:
        authenticate_user = AuthenticateUser(
            user_repository=InMemoryUserRepository())
        authenticate_user.execute(user_login.to_user())
    except UserNotFoundException:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    except InvalidUserCredentialsException:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="Invalid user credentials")
    except PasswordLengthException:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail="Passwords must contain more than 9 characters")
    except UsernameLengthException:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail="Username must contain more than 9 characters")
    return True


def validate_cpf(cpf: str) -> bool:
    if not cpf:
        return False

    cpf = clean(cpf)

    if is_invalid_length(cpf):
        return False

    if are_all_digits_same(cpf):
        return False

    dg1 = calculate_digit(cpf, 10)
    dg2 = calculate_digit(cpf, 11)
    return extract_digit(cpf) == f"{dg1}{dg2}"


def clean(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)


def is_invalid_length(cpf: str) -> bool:
    return len(cpf) != 11


def are_all_digits_same(cpf: str) -> bool:
    return all(c == cpf[0] for c in cpf)

def calculate_digit(cpf: string, factor: int) -> int:
    total = 0
    for digit in cpf:
        if factor > 1:
            factor -= 1
            total += int(digit) * factor
    rest = total%11
    return 0 if rest < 2 else 11 - rest


def extract_digit(cpf: str) -> str:
    return cpf[9:]