from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/reviews/<recipe_id>")
def get_reviews(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400

    reviews = list(db.reviews.find({"recipeId": oid}).sort("reviewDateTime", -1))
    for r in reviews:
        r["_id"]      = str(r["_id"])
        r["userId"]   = str(r["userId"])
        r["recipeId"] = str(r["recipeId"])
    return jsonify(reviews)


@reviews_bp.route("/reviews", methods=["POST"])
def create_review():
    db   = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["userId", "recipeId", "rating"]
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        data["userId"]   = ObjectId(data["userId"])
        data["recipeId"] = ObjectId(data["recipeId"])
    except Exception:
        return jsonify({"error": "Invalid userId or recipeId"}), 400

    if not isinstance(data["rating"], int) or not 1 <= data["rating"] <= 5:
        return jsonify({"error": "rating must be an integer 1–5"}), 400

    data.setdefault("comment", "")
    data["reviewDateTime"] = datetime.now(timezone.utc)
    result = db.reviews.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


@reviews_bp.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    db = get_db()
    try:
        oid = ObjectId(review_id)
    except Exception:
        return jsonify({"error": "Invalid review_id"}), 400

    result = db.reviews.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"deleted": result.deleted_count})
