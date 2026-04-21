from flask import Blueprint, render_template
from app.db import get_db

recipes_bp = Blueprint("recipes", __name__)

@recipes_bp.route("/recipes")
def recipe_list():
    db = get_db()
    recipes = list(db.recipes.find())
    print("Found:", len(recipes), "recipes")
    print("DB name:", db.name)
    return render_template("recipe_list.html", recipes=recipes)

def create_recipe(recipe):
    db = get_db()
    db.execute('INSERT INTO recipe (title, description, categoryid, authoruserid, ingredients, tags, dietaryflags, cooktime, servings) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
               (recipe.title, recipe.description, recipe.categoryid, recipe.authoruserid, recipe.ingredients, recipe.tags, recipe.dietaryflags, recipe.cooktime, recipe.servings))
    db.commit()

def read_recipe(recipe_id: int):
    db = get_db()
    return db.execute('SELECT * FROM recipe WHERE id = ?', (recipe_id,)).fetchone()

def update_recipe(recipe):
    db = get_db()
    db.execute('UPDATE recipe SET title = ?, description = ?, categoryid = ?, authoruserid = ?, ingredients = ?, tags = ?, dietaryflags = ?, cooktime = ?, servings = ? WHERE id = ?',
               (recipe.title, recipe.description, recipe.categoryid, recipe.authoruserid, recipe.ingredients, recipe.tags, recipe.dietaryflags, recipe.cooktime, recipe.servings, recipe.id))
    db.commit()

def delete_recipe(recipe_id: int):
    db = get_db()
    db.execute('DELETE FROM recipe WHERE id = ?', (recipe_id,))
    db.commit()
