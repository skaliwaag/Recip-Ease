from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

# Blueprint for users
users_bp = Blueprint("users", __name__)


def _serialize(user):
    # Convert ObjectId to string for JSON serialization
    user["_id"] = str(user["_id"])
    return user


#--------------------------------
# READ/FIND ALL users
#--------------------------------
@users_bp.route("/users", methods=["GET"])
def get_all_users():
    # Get the database connection
    db = get_db()
    # Get all user documents
    users = list(db.users.find({}, {"name": 1, "email": 1, "dietary_preferences": 1, "created_at": 1}).sort("name", 1))
    # Return the list of users as JSON
    return jsonify([_serialize(u) for u in users]), 200


#-------------------------------------
# READ/FIND ONE user
#-------------------------------------
@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    # Find and return the user document by _id
    user = db.users.find_one({"_id": oid})
    # If user not found, return 404 error
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Return the user document as JSON
    return jsonify(_serialize(user)), 200


#--------------------------------
# CREATE/INSERT user
#--------------------------------
@users_bp.route("/users", methods=["POST"])
def create_user():
    # Get the database connection
    db = get_db()
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve user fields from the JSON data
    required = ["name", "email"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    if db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already registered"}), 409
    data.setdefault("dietary_preferences", [])
    data.setdefault("favorite_categories", [])
    # Set created_at to current time if not provided
    data["created_at"] = datetime.now(timezone.utc)
    # Create the user and get the inserted ID
    result = db.users.insert_one(data)
    # Return the inserted ID as JSON
    return jsonify({"message": "User created successfully", "user_id": str(result.inserted_id)}), 201


#---------------------------------
# UPDATE ONE user
#---------------------------------
@users_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    # Get the JSON data from the request
    data = request.get_json()
    # Build the user update
    allowed = ["name", "email", "dietary_preferences", "favorite_categories"]
    # ensures that only fields with values are updated
    update_fields = {k: v for k, v in data.items() if k in allowed}
    # If no fields to update, return 400 error
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    # Update the user document by _id and return the result
    result = db.users.update_one({"_id": oid}, {"$set": update_fields})
    # If no documents were modified, return 404 error
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "User updated successfully"}), 200


#--------------------------------
# DELETE user
#--------------------------------
@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    # Delete the user document by _id and return the result
    result = db.users.delete_one({"_id": oid})
    # If no documents were deleted, return 404 error
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200
