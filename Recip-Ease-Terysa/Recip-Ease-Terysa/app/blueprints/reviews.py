# fixed: was SQLite-based with no routes; converted to MongoDB (matching the rest of the app)
# and added Flask routes so these functions are actually accessible as API endpoints
from flask import Blueprint, jsonify, request
from app.db import get_db
from datetime import datetime

reviews_bp = Blueprint("reviews", __name__)

#--------------------------------
# CREATE review
#--------------------------------
def create_review(user_id, recipe_id, rating, comment):
    db = get_db()
    review = {
        "user_id": user_id,
        "recipe_id": recipe_id,
        "rating": rating,
        "comment": comment,
        "created_at": datetime.utcnow()
    }
    return db.reviews.insert_one(review).inserted_id

#--------------------------------
# Route for creating a review
#--------------------------------
@reviews_bp.route("/reviews", methods=["POST"])
def create_review_route():
    data = request.get_json()
    user_id = data.get("user_id")
    recipe_id = data.get("recipe_id")
    rating = data.get("rating")
    comment = data.get("comment")
    if not user_id or not recipe_id or rating is None:
        return jsonify({"error": "Missing required fields"}), 400
    review_id = create_review(user_id, recipe_id, rating, comment)
    return jsonify({"message": "Review created", "review_id": str(review_id)}), 201

#--------------------------------
# READ ONE review by user_id
#--------------------------------
def read_review(user_id):
    db = get_db()
    return db.reviews.find_one({"user_id": user_id})

#--------------------------------
# Route for reading a review by user_id
#--------------------------------
@reviews_bp.route("/reviews/<user_id>", methods=["GET"])
def read_review_route(user_id):
    review = read_review(user_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    review["_id"] = str(review["_id"])
    return jsonify(review), 200

#--------------------------------
# UPDATE review
#--------------------------------
def update_review(user_id, recipe_id, rating, comment):
    update_fields = {}
    if recipe_id is not None:
        update_fields["recipe_id"] = recipe_id
    if rating is not None:
        update_fields["rating"] = rating
    if comment is not None:
        update_fields["comment"] = comment
    if not update_fields:
        return None
    db = get_db()
    return db.reviews.update_one({"user_id": user_id}, {"$set": update_fields})

#--------------------------------
# Route for updating a review by user_id
#--------------------------------
@reviews_bp.route("/reviews/<user_id>", methods=["PUT"])
def update_review_route(user_id):
    data = request.get_json()
    recipe_id = data.get("recipe_id")
    rating = data.get("rating")
    comment = data.get("comment")
    result = update_review(user_id, recipe_id, rating, comment)
    if result is None:
        return jsonify({"error": "No fields to update"}), 400
    if result.modified_count == 0:
        return jsonify({"error": "Review not found or no changes made"}), 404
    return jsonify({"message": "Review updated successfully"}), 200

#--------------------------------
# DELETE review
#--------------------------------
def delete_review(user_id):
    db = get_db()
    return db.reviews.delete_one({"user_id": user_id})

#--------------------------------
# Route for deleting a review by user_id
#--------------------------------
@reviews_bp.route("/reviews/<user_id>", methods=["DELETE"])
def delete_review_route(user_id):
    result = delete_review(user_id)
    if result.deleted_count == 0:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"message": "Review deleted successfully"}), 200
