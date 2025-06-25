from typing import cast, overload

from sqlalchemy import select

from application.exceptions import NotFoundError
from domain.entities.entity import Id
from domain.entities.user.role import Role
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName
from domain.repositories.user_repository import IUserRepository
from infrastructure.sqlalchemy.models.role import RoleModel
from infrastructure.sqlalchemy.models.user import UserModel
from infrastructure.sqlalchemy.query_executor import QueryExecutor
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(
        self,
        query_executor: QueryExecutor,
        transaction_manager: SQLAlchemyTransactionManager,
    ):
        self.query_executor = query_executor
        self.transaction_manager = transaction_manager

    def get_by_id(self, user_id: int) -> User:
        statement = (
            select(UserModel, RoleModel)
            .join(RoleModel, UserModel.role_id == RoleModel.id)
            .where(UserModel.id == user_id)
        )
        row = self.query_executor.execute_one(statement)
        if not row:
            raise NotFoundError(user_id, "User")

        user_model = row.UserModel
        role_model = row.RoleModel

        return self._to_domain(user_model, role_model)

    def get_by_username(self, username: str) -> User:
        statement = (
            select(UserModel, RoleModel)
            .join(RoleModel, UserModel.role_id == RoleModel.id)
            .where(UserModel.username == username)
        )
        row = self.query_executor.execute_one(statement)
        if not row:
            raise NotFoundError(username, "User")

        user_model = row.UserModel
        role_model = row.RoleModel

        return self._to_domain(user_model, role_model)

    def exists(self, user_id: int) -> bool:
        statement = select(1).where(UserModel.id == user_id)
        user_model = self.query_executor.execute_scalar_one(statement)
        return bool(user_model)

    def exists_by_username(self, username: str) -> bool:
        statement = select(1).where(UserModel.username == username)
        user_model = self.query_executor.execute_scalar_one(statement)
        return bool(user_model)

    def save(self, user: User) -> User:
        with self.transaction_manager.get_session():
            user_model = self._to_model(user)
            user_model = self.query_executor.save(user_model)
            return self._to_domain(user_model, user_model.role)

    @overload
    def _to_domain(self, model: UserModel, role: Role) -> User: ...
    @overload
    def _to_domain(self, model: UserModel, role: RoleModel) -> User: ...
    def _to_domain(self, model: UserModel, role: Role | RoleModel) -> User:
        return User(
            entity_id=Id(cast(int, model.id)),
            username=cast(str, model.username),
            password_hash=cast(str, model.password_hash),
            full_name=FullName(
                surname=cast(str, model.surname),
                name=cast(str, model.name),
                patronymic=cast(str, model.patronymic),
            ),
            role=(
                Role(
                    entity_id=Id(cast(int, role.id)),
                    name=cast(str, role.name),
                    description=cast(str, role.description),
                )
                if isinstance(role, RoleModel)
                else role
            ),
        )

    def _to_model(self, user: User) -> UserModel:
        return UserModel(
            id=user.id.value if user.id else None,
            username=user.username,
            password_hash=user.password_hash,
            surname=user.full_name.surname,
            name=user.full_name.name,
            patronymic=user.full_name.patronymic,
            role_id=user.role.id_safe.value,
        )
