from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required  # type: ignore
from werkzeug.utils import secure_filename

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
from domain.constants import ALLOWED_TYPES
from presentation.web.flask.forms import RecipeForm, ReviewForm
from presentation.web.flask.main import get_current_user
from presentation.web.flask.utils import get_container


recipes_bp = Blueprint("recipes", __name__)


def allowed_file(filename: str):
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_TYPES
    )


@recipes_bp.route("/<int:recipe_id>")
def recipe_view(recipe_id: int):
    use_case = get_container().get_recipe_uc()
    try:
        recipe_dto = use_case.execute(recipe_id)
        return render_template(
            "recipe_view.html", recipe_dto=recipe_dto, review_form=ReviewForm()
        )
    except NotFoundError:
        flash("Recipe not found.", "error")
        return redirect(url_for("main.index"))
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("main.index"))


@recipes_bp.route("/add", methods=["GET", "POST"])
@login_required
def recipe_add():
    use_case = get_container().create_recipe_uc()

    form = RecipeForm()
    if form.validate_on_submit():  # type: ignore
        try:
            images: list[UploadImageCommand] = []
            for file in request.files.getlist("images"):
                if file and file.filename and allowed_file(file.filename):
                    secure_filename(file.filename)
                    from io import BytesIO

                    images.append(
                        UploadImageCommand(file.mimetype, BytesIO(file.read()))
                    )

            command = CreateRecipeCommand(
                title=form.title.data,  # type: ignore
                description=form.description.data,  # type: ignore
                preparation_time=int(form.preparation_time.data),  # type: ignore
                servings=int(form.servings.data),  # type: ignore
                ingredients=form.ingredients.data,  # type: ignore
                steps=form.steps.data,  # type: ignore
                images=images,
            )

            recipe = use_case.execute(command, get_current_user())

            flash("Recipe created successfully.", "success")
            return redirect(
                url_for("recipes.recipe_view", recipe_id=recipe.id)
            )
        except Exception as e:
            flash(str(e), "error")

    return render_template("recipe_form.html", form=form, action="add")


@recipes_bp.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def recipe_edit(recipe_id: int):
    use_case = get_container().update_recipe_uc()
    get_recipe_uc = get_container().get_recipe_uc()
    try:
        recipe_dto = get_recipe_uc.execute(recipe_id)
    except NotFoundError:
        flash("Recipe not found.", "error")
        return redirect(url_for("main.index"))
    if (
        get_current_user().role.name != "admin"
        and recipe_dto.recipe.author_id != get_current_user().user_id
    ):
        flash("No permission.", "error")
        return redirect(url_for("main.index"))
    form = RecipeForm(obj=recipe_dto.recipe)
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
            use_case.execute(command, get_current_user())
            flash("Recipe updated.", "success")
            return redirect(
                url_for("recipes.recipe_view", recipe_id=recipe_id)
            )
        except Exception as e:
            flash(str(e), "error")
    return render_template(
        "recipe_form.html", form=form, action="edit", recipe_id=recipe_id
    )


@recipes_bp.route("/delete/<int:recipe_id>", methods=["POST"])
@login_required
def recipe_delete(recipe_id: int):
    use_case = get_container().delete_recipe_uc()
    try:
        use_case.execute(recipe_id, get_current_user())
        flash("Recipe deleted.", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("main.index"))


@recipes_bp.route("/<int:recipe_id>/review", methods=["POST"])
@login_required
def review_create(recipe_id: int):
    use_case = get_container().create_review_uc()
    form = ReviewForm()
    if form.validate_on_submit():  # type: ignore
        try:
            command = CreateReviewCommand(
                recipe_id=recipe_id,
                user_id=get_current_user().user_id,
                rating=form.rating.data,
                text=form.text.data,  # type: ignore
            )
            use_case.execute(command, get_current_user())
            flash("Review added.", "success")
        except Exception as e:
            flash(str(e), "error")
    return redirect(url_for("recipes.recipe_view", recipe_id=recipe_id))
