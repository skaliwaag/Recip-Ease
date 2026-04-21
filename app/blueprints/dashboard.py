from flask import Blueprint, jsonify
from app.db import get_db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def get_dashboard():
    db = get_db()

    # 1 — recipes per category
    recipes_per_category = list(db.recipes.aggregate([
        {
            "$lookup": {
                "from":         "categories",
                "localField":   "categoryId",
                "foreignField": "_id",
                "as":           "category"
            }
        },
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {
            "$group": {
                "_id":   "$categoryId",
                "name":  {"$first": "$category.name"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]))

    # 2 — top-rated recipes (avg rating across all reviews)
    top_rated = list(db.recipes.aggregate([
        {
            "$lookup": {
                "from":         "reviews",
                "localField":   "_id",
                "foreignField": "recipeId",
                "as":           "reviews"
            }
        },
        {"$match": {"reviews.0": {"$exists": True}}},
        {
            "$addFields": {
                "avgRating":   {"$avg": "$reviews.rating"},
                "reviewCount": {"$size": "$reviews"}
            }
        },
        {
            "$project": {
                "title": 1,
                "avgRating": 1,
                "reviewCount": 1
            }
        },
        {"$sort": {"avgRating": -1}},
        {"$limit": 5}
    ]))

    # 3 — most bookmarked recipes
    most_saved = list(db.savedRecipes.aggregate([
        {
            "$group": {
                "_id":       "$recipeId",
                "saveCount": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from":         "recipes",
                "localField":   "_id",
                "foreignField": "_id",
                "as":           "recipe"
            }
        },
        {"$unwind": "$recipe"},
        {
            "$project": {
                "_id":       {"$toString": "$_id"},
                "title":     "$recipe.title",
                "saveCount": 1
            }
        },
        {"$sort": {"saveCount": -1}},
        {"$limit": 5}
    ]))

    def str_id(doc):
        doc["_id"] = str(doc["_id"])
        return doc

    return jsonify({
        "recipesPerCategory": [str_id(d) for d in recipes_per_category],
        "topRated":           [str_id(d) for d in top_rated],
        "mostSaved":          most_saved
    })
