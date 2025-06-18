from sqlalchemy.orm import Session

from application.interfaces.services.password_hash_service import (
    IPasswordHasher,
)
from domain.entities.user.role import RoleEnum
from infrastructure.sqlalchemy.initializer.role_seeder import seed_roles
from infrastructure.sqlalchemy.models.user import UserModel


def create_users(session: Session, hasher: IPasswordHasher) -> None:
    seed_roles(session)

    admin = UserModel(
        id=1,
        username="admin",
        password_hash=hasher.hash("12345"),
        surname="doe",
        name="john",
        patronymic="first",
        role_id=RoleEnum.ADMIN.value.id_safe.value,
    )
    user = UserModel(
        id=2,
        username="user",
        password_hash=hasher.hash("12345"),
        surname="doe",
        name="jane",
        patronymic=None,
        role_id=RoleEnum.USER.value.id_safe.value,
    )
    for i in [admin, user]:
        exists = (
            session.query(UserModel).filter_by(username=i.username).first()
        )
        if not exists:
            session.add(i)

    session.commit()
