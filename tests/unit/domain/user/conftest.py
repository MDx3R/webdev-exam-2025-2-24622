from typing import Any

import pytest

from domain.entities.user.dtos import UserData
from domain.entities.user.role import RoleEnum


@pytest.fixture
def valid_user_data() -> dict[str, Any]:
    return {
        "username": "john_doe",
        "password_hash": "hashed_password_123",
        "surname": "Doe",
        "name": "John",
        "patronymic": None,
        "role": RoleEnum.USER.value,
    }


@pytest.fixture
def valid_user_data_dto(valid_user_data: dict[str, Any]) -> UserData:
    return UserData(**valid_user_data)
