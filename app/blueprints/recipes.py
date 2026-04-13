from flask import Blueprint, render_template
from app.db import get_db

recipes_bp = Blueprint("recipes", __name__)

@recipes_bp.route("/recipes")
def recipe_list():
    db = get_db()
    recipes = list(db.recipes.find())
    return render_template("recipe_list.html", recipes=recipes)