from sqlalchemy.orm import Session

from domain.entities.user.role import RoleEnum
from infrastrcuture.sqlalchemy.models.role import RoleModel


def seed_roles(session: Session) -> None:
    for role_enum in RoleEnum:
        role = role_enum.value
        exists = (
            session.query(RoleModel).filter_by(id=role.id_safe.value).first()
        )
        if not exists:
            session.add(
                RoleModel(
                    id=role.id_safe.value,
                    name=role.name,
                    description=role.description,
                )
            )
    session.commit()
