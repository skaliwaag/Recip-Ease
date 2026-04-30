from flask import Blueprint, jsonify
from app.db import get_db
from bson import ObjectId

recommendations_bp = Blueprint("recommendations", __name__)


# ObjectIds can't be serialized to JSON directly — convert them to strings
# before jsonify sees them, otherwise the response throws a TypeError
def _serialize(doc):
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

    # Validate and fetch the user before building the pipeline.
    # ObjectId() raises if user_id isn't a valid 24-hex string, so we
    # catch that separately from a valid-but-missing user.
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Pull the two preference arrays stored on the user document.
    # These drive the $match filter below — recipes are candidates if they
    # match either the user's dietary needs or their preferred categories.
    dietary_prefs  = user.get("dietaryPreferences", [])
    fav_categories = user.get("favoriteCategories", [])

    # Build the $or conditions dynamically so we only include non-empty arrays.
    # $in with an empty list matches nothing, which would silently return zero
    # results even if the other condition has matches.
    conditions = []
    if dietary_prefs:
        # recipe.dietaryFlags is an array — $in checks for any overlap
        conditions.append({"dietaryFlags": {"$in": dietary_prefs}})
    if fav_categories:
        # recipe.categoryId is a single ObjectId reference to the categories collection
        conditions.append({"categoryId": {"$in": fav_categories}})

    # If the user has no preferences at all, fall back to {} which matches every
    # recipe — new users still get results rather than an empty page.
    # $or with an empty array is a MongoDB error, so we can't pass it directly.
    match_filter = {"$or": conditions} if conditions else {}

    pipeline = [
        # Stage 1 — narrow the recipe pool to candidates that match this user's
        # preferences. With no preferences, match_filter is {} so all recipes pass.
        {"$match": match_filter},

        # Stage 2 — join the reviews collection on recipeId, producing an embedded
        # "reviews" array on each recipe document. This avoids a second round-trip
        # to compute ratings — the data is available in memory for stage 3.
        {"$lookup": {
            "from":         "reviews",
            "localField":   "_id",
            "foreignField": "recipeId",
            "as":           "reviews"
        }},

        # Stage 3 — derive avgRating and reviewCount from the joined array.
        # $avg on an empty array returns null (not 0), which is intentional —
        # unrated recipes sort below rated ones rather than appearing tied at 0.
        {"$addFields": {
            "avgRating":   {"$avg":  "$reviews.rating"},
            "reviewCount": {"$size": "$reviews"}
        }},

        # Stage 4 — best-rated recipes first. Null avgRating sorts last in
        # descending order, so unreviewed recipes naturally fall to the bottom.
        {"$sort": {"avgRating": -1}},

        # Stage 5 — return only the top 3 matches
        {"$limit": 3},
    ]

    results = list(db.recipes.aggregate(pipeline))
    return jsonify([_serialize(r) for r in results])
