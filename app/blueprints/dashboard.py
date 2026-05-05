# Advanced Feature 2: summary statistics dashboard.
# GET /dashboard runs three aggregation pipelines and passes the results to the
# dashboard template. No query parameters needed.
from flask import Blueprint, render_template
from app.db import get_db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    db = get_db()

    # Pipeline 1: recipe count per category.
    # $lookup joins categories to resolve each category's display name.
    # preserveNullAndEmptyArrays keeps recipes that have no category assigned,
    # so they still appear in the count rather than getting dropped by $unwind.
    recipes_per_category = list(db.recipes.aggregate([
        {"$lookup": {"from": "categories", "localField": "category_id", "foreignField": "_id", "as": "category"}},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$category_id", "name": {"$first": "$category.name"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]))
    for d in recipes_per_category:
        d["_id"] = str(d["_id"])

    # Pipeline 2: top 5 recipes by average rating.
    # The $match on reviews.0 filters out recipes with no reviews before the average
    # is computed. Without it, $avg on an empty array returns null, and those
    # unreviewed recipes would sort above legitimately rated ones.
    top_rated = list(db.recipes.aggregate([
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "recipe_id", "as": "reviews"}},
        {"$match": {"reviews.0": {"$exists": True}}},
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}, "reviewCount": {"$size": "$reviews"}}},
        {"$project": {"title": 1, "avgRating": 1, "reviewCount": 1}},
        {"$sort": {"avgRating": -1}},
        {"$limit": 5},
    ]))
    for d in top_rated:
        d["_id"] = str(d["_id"])

    # Pipeline 3: top 5 most saved recipes.
    # Starting from saved_recipes and grouping by recipe_id is the natural approach here:
    # we want a count of save events, so we start at the save records rather than
    # joining from recipes and counting back. The $lookup at the end only needs
    # to pull the title for display.
    most_saved = list(db.saved_recipes.aggregate([
        {"$group": {"_id": "$recipe_id", "saveCount": {"$sum": 1}}},
        {"$lookup": {"from": "recipes", "localField": "_id", "foreignField": "_id", "as": "recipe"}},
        {"$unwind": "$recipe"},
        {"$project": {"_id": {"$toString": "$_id"}, "title": "$recipe.title", "saveCount": 1}},
        {"$sort": {"saveCount": -1}},
        {"$limit": 5},
    ]))

    return render_template("dashboard.html",
        recipes_per_category=recipes_per_category,
        top_rated=top_rated,
        most_saved=most_saved,
    )
