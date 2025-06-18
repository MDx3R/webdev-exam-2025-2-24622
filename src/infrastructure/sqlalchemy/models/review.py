from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from infrastructure.sqlalchemy.models.base import Base


class ReviewModel(Base):
    __tablename__ = "Reviews"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(
        Integer, ForeignKey("Recipes.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
