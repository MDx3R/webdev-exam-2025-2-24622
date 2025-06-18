from flask import Blueprint, render_template, request

from presentation.web.flask.utils import get_container


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    use_case = get_container().list_recipes_uc()

    page = int(request.args.get("page", 1))
    recipes = use_case.execute(page=page, per_page=10)

    return render_template("index.html", recipes=recipes, page=page)
