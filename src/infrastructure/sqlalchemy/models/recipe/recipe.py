from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from infrastructure.sqlalchemy.models.base import Base


class RecipeModel(Base):
    __tablename__ = "Recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    preparation_time = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("Users.id"), nullable=False)

    images = relationship(
        "RecipeImageModel", cascade="all, delete-orphan", lazy="joined"
    )
    reviews = relationship(
        "ReviewModel", cascade="all, delete-orphan", lazy="raise"
    )
