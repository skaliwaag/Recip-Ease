from flask import Blueprint, jsonify, request
from app.db import get_db
from datetime import datetime

# Database setup for reviews
reviews_bp = Blueprint("reviews", __name__)

# Database connection and CRUD operations for reviews
# def get_db():
#     conn = sqlite3.connect('mealplans.db')
#     conn.row_factory = sqlite3.Row
#     return conn

#-------------------------------------
# READ/FIND ONE review
#-------------------------------------
def read_one_review(review_id: int):
    # Get the database connection
    db = get_db()
    # Find and return the review document by _id
    return db.reviews.find_one({"_id": review_id})

#-------------------------------------
# Route for reading one review by user_id
#-------------------------------------
@reviews_bp.route("/reviews/<int:user_id>", methods=["GET"])
def read_one_review_route(review_id):
    # Get the document by ID
    review = reviews_bp.read_one_review(review_id)
    # If recipe not found, return the 404 error
    if not review:
        return jsonify({"error": "Review not found"}), 404
    # Convert ObjectID to string for JSON serialization
    review["_id"] = str(review["_id"])
    # Return the recipe document as JSON
    return jsonify(review), 200
    
#-------------------------------------
# READ/FIND ALL reviews
#-------------------------------------
def read_all_reviews():
    # Get the database connection
    db = get_db()
    # Find and return ALL review documents as a list
    return list(db.reviews.find())

#-------------------------------------
# Route for reading all reviews
#-------------------------------------
@reviews_bp.route("/reviews", methods=["GET"])
def read_all_users_route():
    # Get all reviews documents
    reviews = reviews_bp.read_all_reviews()
    # Convert ObjectId to string for JSON serialization
    for review in reviews:
        review["_id"] = str(review["_id"])
    # Return the list of reviews as JSON
    return jsonify(reviews), 200

#-------------------------------------
# CREATE/INSERT review
#-------------------------------------
def create_review(user_id, review_id, recipe_id, rating, comment, created_at):
    # Set created_at to current time if not provided
    if created_at is None:
        created_at = datetime.utcnow()
    # Get the database connection
    db = get_db()
    # Create the review document
    review = {
        "user_id": user_id,
        "review_id": review_id,
        "recipe_id": recipe_id,
        "rating": rating,
        "comment": comment,
        "created_at": created_at
    }
    # Insert and return the inserted ID
    return db.reviews.insert_one(review).inserted_id

#------------------------------
# Route for creating a review
#------------------------------
@reviews_bp.route("/reviews", methods=["POST"])
def create_review_route():
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve user fields from the JSON data
    user_id = data.get("user_id")
    review_id = data.get("review_id")
    recipe_id = data.get("recipe_id")
    rating = data.get("rating")
    comment = data.get("comment")
    created_at = data.get("created_at")
    # Create the review and get the inserted ID
    result = reviews_bp.create_review(user_id, recipe_id, rating, comment, created_at)
    # Return the inserted ID as JSON
    return jsonify({
        "message": "Review created successfully",
        "inserted_id": str(result)
    }), 201

#------------------------------
# UPDATE ONE review
#------------------------------
# Only rating, comment, and created_at can be updated. reviews_id,user_id and recipe_id are are auto incremented primary keys and cannot be updated.
# Can someone definitely check this one? Or I will later, I kept getting distracted while working on this one, please and thanks!
def update_reviews(review_id, user_id, recipe_id, rating, comment, created_at):
    # Build the review update
    update_fields = {}
    # ensures that only fields with values are updated
    if rating:
        update_fields["rating"] = rating
    if comment:
        update_fields["comment"] = comment
    if created_at:
        update_fields["created_at"] = created_at
    if not update_fields:
        return None
    # Get the database connection
    db = get_db()
    # Update the review document by _id and return the result
    return db.reviews.update_one(
        {"_id": review_id},
        {"user_id": user_id,},
        {"recipe_id": recipe_id,},
        {"$set": update_fields})    
    
#------------------------------
# Route for updating a review
#------------------------------
@reviews_bp.route("/reviews/<int:review_id>", methods=["PUT"])
def update_review_route(review_id):
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve review fields from the JSON data
    user_id = data.get("user_id")
    recipe_id = data.get("recipe_id")
    rating = data.get("rating")
    comment = data.get("comment")
    created_at = data.get("created_at")
    # Update the review and get the result
    result = reviews_bp.update_reviews(review_id, user_id, recipe_id, rating, comment, created_at)
    # If no review was updated, return a 400 error
    if result is None:
        return jsonify({"error": "No fields to update"}), 400
    # If review not found, return a 404 error
    if not result:
        return jsonify({"error": "Review not found"}), 404
    # Return a success message as JSON
    return jsonify({"message": "Review updated successfully"}), 200
    
#------------------------------
# DELETE ONE review
#------------------------------
def delete_one_review(review_id: int):
    db = get_db()
    result = db.reviews.delete_one({"_id": review_id})
    return result.deleted_count

#----------------------------------------------
# Route for deleting one review by ID
#----------------------------------------------
@reviews_bp.route("/reviews/<int:reviews_id>", methods=["DELETE"])
def delete_one_review_route(review_id):
    # Delete the review and get the result
    result = reviews_bp.delete_one_review(review_id)
    # If no ID exists, return a 404 error
    if not result:
        return jsonify({"error": "Review not found!"}), 404
    # Return a success message as JSON
    return jsonify({"message": "Review deleted successfully"}), 200

#--------------------------------
# DELETE many reviews
#--------------------------------
def delete_many_recipes(review_ids):
    # Get the database connection
    db = get_db()
    # Delete the review documents by IDs and return the count of deleted documents
    result = db.review.delete_many({"_id": {"$in": review_ids}})
    # Return the count of deleted documents
    return result.deleted_count

#--------------------------------
# Route for deleting many recipes by IDs
#--------------------------------
@reviews_bp.route("/reviews/batch", methods=["DELETE"])
def delete_many_reviews_route():
    # Get the JSON data from the request
    data = request.get_json()
    # Validate that review_ids is provided and is a list
    review_ids = data.get("review_ids")
    # If review_ids is not provided or is not a list, return 400 error
    if not review_ids or not isinstance(review_ids, list):
        return jsonify({"error": "review_ids must be a list of IDs"}), 400
    # Delete the reviews and get the count of deleted documents
    deleted_count = reviews_bp.delete_many_reviews(review_ids)
    # If no documents were deleted, return 404 error
    if deleted_count == 0:
        return jsonify({"error": "No reviews found for the provided IDs"}), 404
    # Return success message with count of deleted reviews as JSON
    return jsonify({"message": f"{deleted_count} reviews deleted successfully"}), 200