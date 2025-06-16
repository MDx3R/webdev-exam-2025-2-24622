from typing import Any

import pytest

from domain.entities.user.dtos import UserData
from domain.entities.user.factories import UserFactory
from domain.entities.user.user import User


class TestUserFactory:
    @pytest.fixture(autouse=True)
    def setup(self, valid_user_data_dto: UserData):
        self.factory = UserFactory()
        self.valid_data = valid_user_data_dto

    def test_create_with_valid_data_sets_correct_attributes(self):
        user = self.factory.create(self.valid_data)
        assert isinstance(user, User)
        assert user.user_id is None
        assert user.username == self.valid_data.username.strip()
        assert user.password_hash == self.valid_data.password_hash.strip()
        assert user.full_name.surname == self.valid_data.surname.strip()
        assert user.full_name.name == self.valid_data.name.strip()
        assert user.full_name.patronymic == self.valid_data.patronymic
        assert user.role == self.valid_data.role

    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("username", "", "Username is required"),
            ("username", "   ", "Username is required"),
            ("password_hash", "", "Password hash is required"),
            ("password_hash", "   ", "Password hash is required"),
            ("surname", "", "Surname and name must not be empty"),
            ("surname", "   ", "Surname and name must not be empty"),
            ("name", "", "Surname and name must not be empty"),
            ("name", "   ", "Surname and name must not be empty"),
            (
                "patronymic",
                "   ",
                "Patronymic must be None or non-empty string",
            ),
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
        data = UserData(**valid_user_data | {field: value})
        with pytest.raises(AssertionError, match=error):
            self.factory.create(data)
