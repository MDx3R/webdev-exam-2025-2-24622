from flask import render_template, request
from flask.views import MethodView

from application.interfaces.usecases.recipe.list_recipes_usecase import (
    IListRecipesUseCase,
)


class IndexView(MethodView):
    def __init__(self, list_recipes_uc: IListRecipesUseCase):
        self.list_recipes_uc = list_recipes_uc

    def get(self):
        page = int(request.args.get("page", 1))
        recipes = self.list_recipes_uc.execute(page=page, per_page=10)
        return render_template("index.html", recipes=recipes, page=page)
