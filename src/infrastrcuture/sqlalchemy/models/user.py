from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from infrastrcuture.sqlalchemy.models.base import Base


class UserModel(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    surname = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    patronymic = Column(String(100), nullable=True)
    role_id = Column(Integer, ForeignKey("Roles.id"), nullable=False)

    role = relationship("RoleModel", lazy="joined")
