from typing import Any

import pytest

from domain.entities.user.role import RoleEnum
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName


@pytest.fixture
def valid_full_name_data() -> dict[str, Any]:
    return {
        "surname": "Doe",
        "name": "John",
        "patronymic": None,
    }


@pytest.fixture
def valid_user_data(valid_full_name_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "username": "john_doe",
        "password_hash": "hashed_password_123",
        "full_name": FullName.create(**valid_full_name_data),
        "role": RoleEnum.USER,
    }


@pytest.fixture
def valid_user(valid_user_data: dict[str, Any]) -> User:
    return User.create(**valid_user_data)


class TestFullName:
    def test_create_with_valid_data_sets_correct_attributes(
        self, valid_full_name_data: dict[str, Any]
    ):
        full_name = FullName.create(**valid_full_name_data)
        assert full_name.surname == valid_full_name_data["surname"].strip()
        assert full_name.name == valid_full_name_data["name"].strip()
        assert full_name.patronymic == valid_full_name_data["patronymic"]
        assert full_name.short() == "Doe J."
        assert full_name.full() == "Doe John"

    def test_create_with_non_empty_patronymic(self):
        data = {"surname": "Doe", "name": "John", "patronymic": "Smith"}
        full_name = FullName.create(**data)
        assert full_name.patronymic == "Smith"
        assert full_name.full() == "Doe John Smith"

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("surname", "", "Surname and name must not be empty"),
            ("surname", "   ", "Surname and name must not be empty"),
            ("name", "", "Surname and name must not be empty"),
            ("name", "   ", "Surname and name must not be empty"),
            (
                "patronymic",
                "   ",
                "Patronymic must be None or non-empty string",
            ),
        ],
    )
    def test_create_with_invalid_data_raises_assertion(
        self,
        valid_full_name_data: dict[str, Any],
        field: str,
        value: Any,
        error: str,
    ):
        data = valid_full_name_data | {field: value}
        with pytest.raises(AssertionError, match=error):
            FullName.create(**data)


class TestUser:
    @pytest.fixture(autouse=True)
    def setup(self, valid_user: User):
        self.user = valid_user

    def test_create_with_valid_data_sets_correct_attributes(
        self, valid_user_data: dict[str, Any]
    ):
        user = User.create(**valid_user_data)
        assert user.user_id is None
        assert user.username == valid_user_data["username"]
        assert user.password_hash == valid_user_data["password_hash"]
        assert user.full_name == valid_user_data["full_name"]
        assert user.role == valid_user_data["role"]

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("username", "", "Username is required"),
            ("username", "   ", "Username is required"),
            ("password_hash", "", "Password hash is required"),
            ("password_hash", "   ", "Password hash is required"),
            ("full_name", None, "Full name is required"),
            ("role", None, "Role is required"),
        ],
    )
    def test_create_with_invalid_data_raises_assertion(
        self,
        valid_user_data: dict[str, Any],
        field: str,
        value: Any,
        error: str,
    ):
        data = valid_user_data | {field: value}
        with pytest.raises(AssertionError, match=error):
            User.create(**data)
