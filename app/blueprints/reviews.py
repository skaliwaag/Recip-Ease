# JSON API for review CRUD operations.
# Reviews link a user to a recipe with a 1-5 integer rating and an optional comment.
from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

reviews_bp = Blueprint("reviews", __name__)


def _serialize(review):
    # Stringify ObjectIds so the response is valid JSON
    review["_id"] = str(review["_id"])
    if "user_id" in review:
        review["user_id"] = str(review["user_id"])
    if "recipe_id" in review:
        review["recipe_id"] = str(review["recipe_id"])
    return review


# ── GET ALL REVIEWS ──
# Returns all reviews sorted by date, newest first.
@reviews_bp.route("/reviews", methods=["GET"])
def get_all_reviews():
    db = get_db()
    reviews = list(db.reviews.find().sort("created_at", -1))
    return jsonify([_serialize(r) for r in reviews]), 200


# ── GET REVIEWS FOR A RECIPE ──
# Returns every review for one recipe, sorted newest first.
@reviews_bp.route("/reviews/<recipe_id>", methods=["GET"])
def get_reviews_for_recipe(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    reviews = list(db.reviews.find({"recipe_id": oid}).sort("created_at", -1))
    return jsonify([_serialize(r) for r in reviews]), 200


# ── CREATE REVIEW ──
# rating must be a whole-number integer between 1 and 5. The isinstance check
# catches floats like 4.5, which would pass a plain range check but aren't valid.
@reviews_bp.route("/reviews", methods=["POST"])
def create_review():
    db = get_db()
    data = request.get_json()
    required = ["user_id", "recipe_id", "rating"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    try:
        data["user_id"] = ObjectId(data["user_id"])
        data["recipe_id"] = ObjectId(data["recipe_id"])
    except Exception:
        return jsonify({"error": "Invalid user_id or recipe_id"}), 400
    if not isinstance(data["rating"], int) or not 1 <= data["rating"] <= 5:
        return jsonify({"error": "rating must be an integer 1-5"}), 400
    data.setdefault("comment", "")
    # Set server-side so the client can't pass in a fake timestamp
    data["created_at"] = datetime.now(timezone.utc)
    result = db.reviews.insert_one(data)
    return jsonify({"message": "Review created successfully", "inserted_id": str(result.inserted_id)}), 201


# ── UPDATE REVIEW ──
# Only rating and comment can be changed after submission. user_id, recipe_id,
# and created_at are fixed once a review is created.
@reviews_bp.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    db = get_db()
    try:
        oid = ObjectId(review_id)
    except Exception:
        return jsonify({"error": "Invalid review_id"}), 400
    data = request.get_json()
    allowed = ["rating", "comment"]
    update_fields = {k: v for k, v in data.items() if k in allowed}
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    if "rating" in update_fields:
        if not isinstance(update_fields["rating"], int) or not 1 <= update_fields["rating"] <= 5:
            return jsonify({"error": "rating must be an integer 1-5"}), 400
    result = db.reviews.update_one({"_id": oid}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"message": "Review updated successfully"}), 200


# ── DELETE REVIEW ──
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
    return jsonify({"message": "Review deleted successfully"}), 200
