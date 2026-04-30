from flask import Blueprint, jsonify
from app.db import get_db
from bson import ObjectId

recommendations_bp = Blueprint("recommendations", __name__)


def _serialize(doc):
    # ObjectIds aren't JSON-serializable — convert everything to strings
    doc["_id"] = str(doc["_id"])
    if "categoryId" in doc:
        doc["categoryId"] = str(doc["categoryId"])
    if "authorUserId" in doc:
        doc["authorUserId"] = str(doc["authorUserId"])
    for review in doc.get("reviews", []):
        review["_id"]      = str(review["_id"])
        review["userId"]   = str(review["userId"])
        review["recipeId"] = str(review["recipeId"])
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

    dietary_prefs  = user.get("dietaryPreferences", [])
    fav_categories = user.get("favoriteCategories", [])

    # only add conditions for non-empty arrays — $in with [] matches nothing
    conditions = []
    if dietary_prefs:
        conditions.append({"dietaryFlags": {"$in": dietary_prefs}})
    if fav_categories:
        conditions.append({"categoryId": {"$in": fav_categories}})

    # {} matches everything, so users with no preferences still get results
    match_filter = {"$or": conditions} if conditions else {}

    pipeline = [
        {"$match": match_filter},
        # join reviews so we can compute avgRating in the next stage
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "recipeId", "as": "reviews"}},
        # $avg on an empty array returns null, so unreviewed recipes sort last
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}, "reviewCount": {"$size": "$reviews"}}},
        {"$sort": {"avgRating": -1}},
        {"$limit": 3},
    ]

    results = list(db.recipes.aggregate(pipeline))
    return jsonify([_serialize(r) for r in results])
