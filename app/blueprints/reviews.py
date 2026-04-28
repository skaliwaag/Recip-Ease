from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

# Database setup for reviews
reviews_bp = Blueprint("reviews", __name__)


def _serialize(review):
    # Convert ObjectId to string for JSON serialization
    review["_id"] = str(review["_id"])
    if "user_id" in review:
        review["user_id"] = str(review["user_id"])
    if "recipe_id" in review:
        review["recipe_id"] = str(review["recipe_id"])
    return review


#-------------------------------------
# READ/FIND ALL reviews
#-------------------------------------
@reviews_bp.route("/reviews", methods=["GET"])
def get_all_reviews():
    # Get the database connection
    db = get_db()
    # Get all reviews documents
    reviews = list(db.reviews.find().sort("created_at", -1))
    # Return the list of reviews as JSON
    return jsonify([_serialize(r) for r in reviews]), 200


#-------------------------------------
# READ/FIND ONE review
#-------------------------------------
@reviews_bp.route("/reviews/<recipe_id>", methods=["GET"])
def get_reviews_for_recipe(recipe_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    # Find and return the review document by recipe_id
    reviews = list(db.reviews.find({"recipe_id": oid}).sort("created_at", -1))
    # Return the review document as JSON
    return jsonify([_serialize(r) for r in reviews]), 200


#-------------------------------------
# CREATE/INSERT review
#-------------------------------------
@reviews_bp.route("/reviews", methods=["POST"])
def create_review():
    # Get the database connection
    db = get_db()
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve user fields from the JSON data
    required = ["user_id", "recipe_id", "rating"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    try:
        data["user_id"] = ObjectId(data["user_id"])
        data["recipe_id"] = ObjectId(data["recipe_id"])
    except Exception:
        return jsonify({"error": "Invalid user_id or recipe_id"}), 400
    # checking isinstance because 4.5 would pass a plain range check but isn't a valid rating
    if not isinstance(data["rating"], int) or not 1 <= data["rating"] <= 5:
        return jsonify({"error": "rating must be an integer 1-5"}), 400
    data.setdefault("comment", "")
    # set here so users can't send in a fake timestamp
    data["created_at"] = datetime.now(timezone.utc)
    # Create the review and get the inserted ID
    result = db.reviews.insert_one(data)
    # Return the inserted ID as JSON
    return jsonify({"message": "Review created successfully", "inserted_id": str(result.inserted_id)}), 201


#------------------------------
# UPDATE ONE review
#------------------------------
# Only rating, comment, and created_at can be updated. reviews_id,user_id and recipe_id are are auto incremented primary keys and cannot be updated.
# Can someone definitely check this one? Or I will later, I kept getting distracted while working on this one, please and thanks!
@reviews_bp.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(review_id)
    except Exception:
        return jsonify({"error": "Invalid review_id"}), 400
    # Get the JSON data from the request
    data = request.get_json()
    # Build the review update
    allowed = ["rating", "comment"]
    # ensures that only fields with values are updated
    update_fields = {k: v for k, v in data.items() if k in allowed}
    # If no fields to update, return 400 error
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    if "rating" in update_fields:
        if not isinstance(update_fields["rating"], int) or not 1 <= update_fields["rating"] <= 5:
            return jsonify({"error": "rating must be an integer 1-5"}), 400
    # Update the review document by _id and return the result
    result = db.reviews.update_one({"_id": oid}, {"$set": update_fields})
    # If no documents were modified, return 404 error
    if result.matched_count == 0:
        return jsonify({"error": "Review not found"}), 404
    # Return a success message as JSON
    return jsonify({"message": "Review updated successfully"}), 200


#----------------------------------------------
# DELETE ONE review
#----------------------------------------------
@reviews_bp.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(review_id)
    except Exception:
        return jsonify({"error": "Invalid review_id"}), 400
    # Delete the review and get the result
    result = db.reviews.delete_one({"_id": oid})
    # If no ID exists, return a 404 error
    if result.deleted_count == 0:
        return jsonify({"error": "Review not found"}), 404
    # Return a success message as JSON
    return jsonify({"message": "Review deleted successfully"}), 200
