from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    db = get_db()
    q        = request.args.get("q", "").strip()
    flag     = request.args.get("flag", "").strip()
    category = request.args.get("category", "").strip()

    query = {}
    if q:
        query["$text"] = {"$search": q}
    if flag:
        query["dietaryFlags"] = flag
    if category:
        try:
            query["categoryId"] = ObjectId(category)
        except Exception:
            pass

    recipes = list(db.recipes.find(query).sort("title", 1))
    for r in recipes:
        r["_id"] = str(r["_id"])

    categories = list(db.categories.find({}).sort("name", 1))
    for c in categories:
        c["_id"] = str(c["_id"])

    dietary_flags = ["vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free"]

    return render_template("index.html",
                           recipes=recipes,
                           categories=categories,
                           dietary_flags=dietary_flags,
                           q=q, flag=flag, category=category)


@views_bp.route("/recipe/new", methods=["GET", "POST"])
def recipe_new():
    db = get_db()
    if request.method == "POST":
        f = request.form
        try:
            category_oid = ObjectId(f["categoryId"])
            author_oid   = ObjectId(f["authorUserId"])
        except Exception:
            flash("Invalid category or author selection.", "danger")
            return redirect(url_for("views.recipe_new"))

        tags          = [t.strip() for t in f.get("tags", "").split(",") if t.strip()]
        dietary_flags = request.form.getlist("dietaryFlags")

        db.recipes.insert_one({
            "title":        f["title"],
            "description":  f["description"],
            "categoryId":   category_oid,
            "authorUserId": author_oid,
            "ingredients":  [{"name": i.strip()} for i in f.get("ingredients", "").split("\n") if i.strip()],
            "prepTime":     int(f.get("prepTime", 0)),
            "cookTime":     int(f.get("cookTime", 0)),
            "servings":     int(f.get("servings", 1)),
            "tags":         tags,
            "dietaryFlags": dietary_flags,
        })
        return redirect(url_for("views.index"))

    categories = list(db.categories.find({}).sort("name", 1))
    for c in categories:
        c["_id"] = str(c["_id"])

    users = list(db.users.find({}, {"name": 1}).sort("name", 1))
    for u in users:
        u["_id"] = str(u["_id"])

    dietary_flags = ["vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free"]

    return render_template("recipe_form.html",
                           categories=categories,
                           users=users,
                           dietary_flags=dietary_flags)


@views_bp.route("/recipe/<recipe_id>")
def recipe_detail(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return "Invalid recipe ID", 400

    pipeline = [
        {"$match": {"_id": oid}},
        {"$lookup": {"from": "categories", "localField": "categoryId",   "foreignField": "_id", "as": "category"}},
        {"$lookup": {"from": "users",      "localField": "authorUserId", "foreignField": "_id", "as": "author"}},
        {"$lookup": {"from": "reviews",    "localField": "_id",          "foreignField": "recipeId", "as": "reviews"}},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$author",   "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}}},
    ]
    results = list(db.recipes.aggregate(pipeline))
    if not results:
        return "Recipe not found", 404

    recipe = results[0]
    recipe["_id"]          = str(recipe["_id"])
    recipe["categoryId"]   = str(recipe.get("categoryId", ""))
    recipe["authorUserId"] = str(recipe.get("authorUserId", ""))
    if "category" in recipe:
        recipe["category"]["_id"] = str(recipe["category"]["_id"])
    if "author" in recipe:
        recipe["author"]["_id"] = str(recipe["author"]["_id"])
    for r in recipe.get("reviews", []):
        r["_id"]      = str(r["_id"])
        r["userId"]   = str(r["userId"])
        r["recipeId"] = str(r["recipeId"])

    users = list(db.users.find({}, {"name": 1}).sort("name", 1))
    for u in users:
        u["_id"] = str(u["_id"])

    return render_template("recipe_detail.html", recipe=recipe, users=users)


@views_bp.route("/recipe/<recipe_id>/delete", methods=["POST"])
def recipe_delete(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return "Invalid recipe ID", 400
    db.recipes.delete_one({"_id": oid})
    return redirect(url_for("views.index"))


@views_bp.route("/recipe/<recipe_id>/review", methods=["POST"])
def review_create(recipe_id):
    db = get_db()
    f  = request.form
    try:
        recipe_oid = ObjectId(recipe_id)
        user_oid   = ObjectId(f["userId"])
        rating     = int(f["rating"])
    except Exception:
        flash("Invalid review data.", "danger")
        return redirect(url_for("views.recipe_detail", recipe_id=recipe_id))

    if not 1 <= rating <= 5:
        flash("Rating must be between 1 and 5.", "danger")
        return redirect(url_for("views.recipe_detail", recipe_id=recipe_id))

    db.reviews.insert_one({
        "recipeId":       recipe_oid,
        "userId":         user_oid,
        "rating":         rating,
        "comment":        f.get("comment", ""),
        "reviewDateTime": datetime.now(timezone.utc),
    })
    return redirect(url_for("views.recipe_detail", recipe_id=recipe_id))


@views_bp.route("/review/<review_id>/delete", methods=["POST"])
def review_delete(review_id):
    db        = get_db()
    recipe_id = request.form.get("recipe_id", "")
    try:
        db.reviews.delete_one({"_id": ObjectId(review_id)})
    except Exception:
        pass
    return redirect(url_for("views.recipe_detail", recipe_id=recipe_id))


@views_bp.route("/stats")
def stats():
    db = get_db()

    recipes_per_category = list(db.recipes.aggregate([
        {"$lookup": {"from": "categories", "localField": "categoryId", "foreignField": "_id", "as": "category"}},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$categoryId", "name": {"$first": "$category.name"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]))
    for d in recipes_per_category:
        d["_id"] = str(d["_id"])

    top_rated = list(db.recipes.aggregate([
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "recipeId", "as": "reviews"}},
        {"$match": {"reviews.0": {"$exists": True}}},
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}, "reviewCount": {"$size": "$reviews"}}},
        {"$project": {"title": 1, "avgRating": 1, "reviewCount": 1}},
        {"$sort": {"avgRating": -1}},
        {"$limit": 5},
    ]))
    for d in top_rated:
        d["_id"] = str(d["_id"])

    most_saved = list(db.savedRecipes.aggregate([
        {"$group": {"_id": "$recipeId", "saveCount": {"$sum": 1}}},
        {"$lookup": {"from": "recipes", "localField": "_id", "foreignField": "_id", "as": "recipe"}},
        {"$unwind": "$recipe"},
        {"$project": {"title": "$recipe.title", "saveCount": 1}},
        {"$sort": {"saveCount": -1}},
        {"$limit": 5},
    ]))
    for d in most_saved:
        d["_id"] = str(d["_id"])

    return render_template("dashboard.html",
                           recipes_per_category=recipes_per_category,
                           top_rated=top_rated,
                           most_saved=most_saved)
