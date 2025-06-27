from io import BytesIO
from typing import ClassVar

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.views import MethodView
from flask_login import login_required  # type: ignore

from application.commands.recipe.create_recipe_command import (
    CreateRecipeCommand,
)
from application.commands.recipe.update_recipe_command import (
    UpdateRecipeCommand,
)
from application.commands.recipe.upload_image_command import UploadImageCommand
from application.commands.review.create_review_command import (
    CreateReviewCommand,
)
from application.exceptions import NotFoundError
from application.interfaces.usecases.recipe.create_recipe_usecase import (
    ICreateRecipeUseCase,
)
from application.interfaces.usecases.recipe.delete_recipe_usecase import (
    IDeleteRecipeUseCase,
)
from application.interfaces.usecases.recipe.get_recipe_by_id_usecase import (
    IGetRecipeByIdUseCase,
)
from application.interfaces.usecases.recipe.update_recipe_usecase import (
    IUpdateRecipeUseCase,
)
from application.interfaces.usecases.review.create_review_usecase import (
    ICreateReviewUseCase,
)
from domain.constants import ALLOWED_TYPES
from domain.entities.user.role import RoleEnum
from presentation.presentators.markdown_renderer import IMarkdownRenderer
from presentation.web.flask.forms import RecipeForm, ReviewForm
from presentation.web.flask.utils import get_current_user


def allowed_file(filename: str):
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_TYPES
    )


class RecipeView(MethodView):
    def __init__(
        self,
        get_recipe_uc: IGetRecipeByIdUseCase,
        markdown_renderer: IMarkdownRenderer,
    ):
        self.get_recipe_uc = get_recipe_uc
        self.markdown_renderer = markdown_renderer

    def get(self, recipe_id: int):
        try:
            recipe_dto = self.get_recipe_uc.execute(recipe_id)
            recipe_dto = self.markdown_renderer.render_full_recipe(recipe_dto)
            return render_template(
                "recipe_view.html",
                recipe_dto=recipe_dto,
                review_form=ReviewForm(),
            )
        except NotFoundError:
            flash("Recipe not found.", "error")
        except Exception as e:

            flash(str(e), "error")
        return redirect(url_for("main.index"))


class RecipeAddView(MethodView):
    decorators: ClassVar = [login_required]  # type: ignore

    def __init__(self, create_recipe_uc: ICreateRecipeUseCase):
        self.create_recipe_uc = create_recipe_uc

    def get(self):
        return render_template(
            "recipe_form.html", form=RecipeForm(), action="add"
        )

    def post(self):
        form = RecipeForm()
        if form.validate_on_submit():  # type: ignore
            try:
                images = [
                    UploadImageCommand(file.mimetype, BytesIO(file.read()))
                    for file in request.files.getlist("images")
                    if file and file.filename and allowed_file(file.filename)
                ]

                command = CreateRecipeCommand(
                    title=form.title.data,  # type: ignore
                    description=form.description.data,  # type: ignore
                    preparation_time=int(form.preparation_time.data),  # type: ignore
                    servings=int(form.servings.data),  # type: ignore
                    ingredients=form.ingredients.data,  # type: ignore
                    steps=form.steps.data,  # type: ignore
                    images=images,
                )

                recipe = self.create_recipe_uc.execute(
                    command, get_current_user()
                )
                flash("Recipe created successfully.", "success")
                return redirect(
                    url_for("recipes.recipe_view", recipe_id=recipe.id)
                )
            except Exception as e:
                flash(str(e), "error")

        return render_template("recipe_form.html", form=form, action="add")


class RecipeEditView(MethodView):
    decorators: ClassVar = [login_required]  # type: ignore

    def __init__(
        self,
        update_recipe_uc: IUpdateRecipeUseCase,
        get_recipe_uc: IGetRecipeByIdUseCase,
    ):
        self.update_recipe_uc = update_recipe_uc
        self.get_recipe_uc = get_recipe_uc

    def get(self, recipe_id: int):
        try:
            recipe_dto = self.get_recipe_uc.execute(recipe_id)
        except NotFoundError:
            flash("Recipe not found.", "error")
            return redirect(url_for("main.index"))

        if (
            get_current_user().role.name != RoleEnum.ADMIN.value.name
            and recipe_dto.recipe.author_id != get_current_user().user_id
        ):
            flash("No permission.", "error")
            return redirect(url_for("main.index"))

        form = RecipeForm(obj=recipe_dto.recipe)
        return render_template(
            "recipe_form.html", form=form, action="edit", recipe_id=recipe_id
        )

    def post(self, recipe_id: int):
        form = RecipeForm()
        if form.validate_on_submit():  # type: ignore
            try:
                command = UpdateRecipeCommand(
                    recipe_id=recipe_id,
                    title=form.title.data,  # type: ignore
                    description=form.description.data,  # type: ignore
                    preparation_time=int(form.preparation_time.data),  # type: ignore
                    servings=int(form.servings.data),  # type: ignore
                    ingredients=form.ingredients.data,  # type: ignore
                    steps=form.steps.data,  # type: ignore
                )
                self.update_recipe_uc.execute(command, get_current_user())
                flash("Recipe updated.", "success")
                return redirect(
                    url_for("recipes.recipe_view", recipe_id=recipe_id)
                )
            except Exception as e:
                flash(str(e), "error")

        return render_template(
            "recipe_form.html", form=form, action="edit", recipe_id=recipe_id
        )


class RecipeDeleteView(MethodView):
    decorators: ClassVar = [login_required]  # type: ignore

    def __init__(self, delete_recipe_uc: IDeleteRecipeUseCase):
        self.delete_recipe_uc = delete_recipe_uc

    def post(self, recipe_id: int):
        try:
            self.delete_recipe_uc.execute(recipe_id, get_current_user())
            flash("Recipe deleted.", "success")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("main.index"))


class ReviewCreateView(MethodView):
    decorators: ClassVar = [login_required]  # type: ignore

    def __init__(self, create_review_uc: ICreateReviewUseCase):
        self.create_review_uc = create_review_uc

    def post(self, recipe_id: int):
        form = ReviewForm()
        if form.validate_on_submit():  # type: ignore
            try:
                command = CreateReviewCommand(
                    recipe_id=recipe_id,
                    user_id=get_current_user().user_id,
                    rating=int(form.rating.data),
                    text=form.text.data,  # type: ignore
                )
                self.create_review_uc.execute(command, get_current_user())
                flash("Review added.", "success")
            except Exception as e:
                flash(str(e), "error")
        return redirect(url_for("recipes.recipe_view", recipe_id=recipe_id))
