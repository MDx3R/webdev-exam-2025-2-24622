from sqlalchemy import Column, ForeignKey, Integer, String

from infrastrcuture.sqlalchemy.models.base import Base


class RecipeImageModel(Base):
    __tablename__ = "RecipeImages"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    recipe_id = Column(
        Integer, ForeignKey("Recipes.id", ondelete="CASCADE"), nullable=False
    )
