from flask_wtf import FlaskForm  # type: ignore
from flask_wtf.file import FileAllowed  # type: ignore
from wtforms import (
    BooleanField,
    FileField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, InputRequired, NumberRange

from domain.constants import ALLOWED_TYPES


class RecipeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    preparation_time = IntegerField(
        "Preparation Time (minutes)",
        validators=[DataRequired(), NumberRange(min=1)],
    )
    servings = IntegerField(
        "Servings", validators=[DataRequired(), NumberRange(min=1)]
    )
    ingredients = TextAreaField("Ingredients", validators=[DataRequired()])
    steps = TextAreaField("Steps", validators=[DataRequired()])
    images = FileField("Images", validators=[FileAllowed(ALLOWED_TYPES)])


class ReviewForm(FlaskForm):
    rating = SelectField(
        "Rating",
        choices=[
            (5, "Excellent"),
            (4, "Good"),
            (3, "Satisfactory"),
            (2, "Unsatisfactory"),
            (1, "Poor"),
            (0, "Terrible"),
        ],
        coerce=int,
        default=5,
        validators=[
            InputRequired()
        ],  # fix: DataRequired doesn't process "Terrible" mark properly because of 0
    )
    text = TextAreaField("Review", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
