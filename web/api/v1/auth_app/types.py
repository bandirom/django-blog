from datetime import date
from typing import NamedTuple, TypedDict

from main.models import GenderChoice


class PasswordResetConfirmData(NamedTuple):
    uid: str
    token: str
    password_1: str
    password_2: str


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str
    birthday: date = None
    gender: GenderChoice = None


class PasswordResetDTO(NamedTuple):
    uid: str
    token: str
