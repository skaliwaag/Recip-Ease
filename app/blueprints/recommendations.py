# Advanced Feature 1: recommendation engine.
# GET /recommendations/<user_id> returns up to 3 recipes matched to a user's
# dietary preferences and favorite categories, ranked by average rating.
from flask import Blueprint, jsonify
from app.db import get_db
from bson import ObjectId

recommendations_bp = Blueprint("recommendations", __name__)


def _serialize(doc):
    # Stringify all ObjectId fields before returning as JSON
    doc["_id"] = str(doc["_id"])
    if "category_id" in doc:
        doc["category_id"] = str(doc["category_id"])
    if "author_user_id" in doc:
        doc["author_user_id"] = str(doc["author_user_id"])
    for review in doc.get("reviews", []):
        review["_id"]       = str(review["_id"])
        review["user_id"]   = str(review["user_id"])
        review["recipe_id"] = str(review["recipe_id"])
    return doc


@recommendations_bp.route("/recommendations/<user_id>")
def get_recommendations(user_id):
    db = get_db()

    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    dietary_prefs  = user.get("dietary_preferences", [])
    fav_categories = user.get("favorite_categories", [])

    # Build a filter that matches recipes by dietary flag OR favorite category.
    # We only add a condition when the array is non-empty because $in: [] matches nothing,
    # which would return zero results instead of falling back to all recipes.
    # If neither list has any entries, match_filter stays as {} and the pipeline
    # runs against all recipes, so new users still get results.
    conditions = []
    if dietary_prefs:
        conditions.append({"dietary_flags": {"$in": dietary_prefs}})
    if fav_categories:
        conditions.append({"category_id": {"$in": fav_categories}})
    match_filter = {"$or": conditions} if conditions else {}

    pipeline = [
        # Stage 1: filter to recipes that match the user's preferences
        {"$match": match_filter},
        # Stage 2: join the reviews collection so we can compute an average rating
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "recipe_id", "as": "reviews"}},
        # Stage 3: compute avgRating and reviewCount from the joined array.
        # $avg on an empty array returns null, which sorts below any real rating.
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}, "reviewCount": {"$size": "$reviews"}}},
        # Stages 4-5: return the top 3 by rating
        {"$sort": {"avgRating": -1}},
        {"$limit": 3},
    ]

    results = list(db.recipes.aggregate(pipeline))
    return jsonify([_serialize(r) for r in results])
