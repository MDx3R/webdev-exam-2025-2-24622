from sqlalchemy import Column, Integer, String, Text

from infrastrcuture.sqlalchemy.models.base import Base


class RoleModel(Base):
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
