from flask import Blueprint, jsonify, request
from app.db import get_db
from datetime import datetime

# Blueprint for users
users_bp = Blueprint("users", __name__)

#-------------------------------------
# READ/FIND ONE user 
#-------------------------------------
def read_one_user(name: str):
    # Get the database connection
    db = get_db()
    # Find and return the user document by name
    return db.users.find_one({"name": name})

#-------------------------------------
# Route for reading one user by name
#-------------------------------------
@users_bp.route("/users/<name>", methods=["GET"])
def read_one_user_route(name):
    # Get the user document by name
    user = users_bp.find_one_user(name)
    # If user not found, return 404 error
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Convert ObjectId to string for JSON serialization
    user["_id"] = str(user["_id"])
    # Return the user document as JSON
    return jsonify(user), 200

#--------------------------------
# READ/FIND ALL users
#--------------------------------
def read_all_users():
    # Get the database connection
    db = get_db()
    # Find and return ALL user documents as a list
    return list(db.users.find())

#--------------------------------
# Route for reading all users
#--------------------------------
@users_bp.route("/users", methods=["GET"])
def read_all_users_route():
    # Get all user documents
    users = users_bp.read_all_users()
    # Convert ObjectId to string for JSON serialization
    for user in users:
        user["_id"] = str(user["_id"])
    # Return the list of users as JSON
    return jsonify(users), 200

#--------------------------------
# CREATE/INSERT user
#--------------------------------
def create_user(name, email, dietary_preferences, favorite_categories, created_at):
    # Set created_at to current time if not provided
    if created_at is None:
        created_at = datetime.utcnow()
    # Get the database connection
    db = get_db()
    # Create a user document
    user = {
        "name": name,
        "email": email,
        "dietary_preferences": dietary_preferences,
        "favorite_categories": favorite_categories,
        "created_at": created_at
    }
    # Insert and return the inserted ID
    return db.users.insert_one(user).inserted_id

#--------------------------------
# Route for creating a user
#--------------------------------
@users_bp.route("/users", methods=["POST"])
def create_user_route():
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve user fields from the JSON data
    name = data.get("name")
    email = data.get("email")
    dietary_preferences = data.get("dietary_preferences")
    favorite_categories = data.get("favorite_categories")
    created_at = data.get("created_at")  # Optional, can be None
    # Create the user and get the inserted ID
    result = users_bp.create_user(name, email, dietary_preferences, favorite_categories, created_at)
    # Return the inserted ID as JSON
    return jsonify({
        "message": "User created successfully",
        "user_id": str(result)  # Convert ObjectId to string for JSON serialization
    }), 201

# CREATE/INSERT many users
# Gonna have to recheck this one, not sure if its right...
# def create_many_users(users):
#     db = get_db()
#     user_docs = []
#     for user in users:
#         user_doc = {
#             "name": user.name,
#             "email": user.email,
#             "dietary_preferences": user.dietary_preferences,
#             "favorite_categories": user.favorite_categories,
#             "created_at": user.created_at or datetime.utcnow()
#         }
#         user_docs.append(user_doc)
#     result = db.users.insert_many(user_docs)
#     return result.inserted_ids

#---------------------------------
# UPDATE ONE user
#---------------------------------
def update_user(name, email, dietary_preferences, favorite_categories):
    # Build the user update
    update_fields = {}
    # ensures that only fields with values are updated
    if email is not None:
        update_fields["email"] = email
    if dietary_preferences is not None:
        update_fields["dietary_preferences"] = dietary_preferences
    if favorite_categories is not None:
        update_fields["favorite_categories"] = favorite_categories
    if not update_fields:
        return None  # No fields to update
    # Get the database connection
    db = get_db()
    # Update the user document by name and return the result
    return db.users.update_one(
        {"name": name}, 
        {"$set": update_fields})

#---------------------------------
# Route for updating a user by name
#---------------------------------
@users_bp.route("/users/<name>", methods=["PUT"])
def update_user_route(name):
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve user fields from the JSON data
    email = data.get("email")
    dietary_preferences = data.get("dietary_preferences")
    favorite_categories = data.get("favorite_categories")
    # Update the user and get the result
    result = users_bp.update_user(name, email, dietary_preferences, favorite_categories)
    # If no fields were updated, return 400 error
    if result is None:
        return jsonify({"error": "No fields to update"}), 400
    # If no documents were modified, return 404 error
    if result.modified_count == 0:
        return jsonify({"error": "User not found or no changes made"}), 404
    # Return success message as JSON
    return jsonify({"message": "User updated successfully"}), 200

# UPDATE many users
# do we even need this? not sure how we would use it, but maybe for batch updates? Why would we need to update many users at once?
#def update_many_users(users):

#--------------------------------
# DELETE user
#--------------------------------
def delete_user(name: str):
    # Get the database connection
    db = get_db()
    # Delete the user document by name and return the result
    db.users.delete_one({"name": name})

#--------------------------------
# Route for deleting a user by name
#--------------------------------
@users_bp.route("/users/<name>", methods=["DELETE"])
def delete_user_route(name):
    # Delete the user and get the result
    result = users_bp.delete_user(name)
    # If no documents were deleted, return 404 error
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200

# # DELETE all users
# # Should I even include this? We can accidentally delete all users with one function...
# def delete_all_users():
#     # Get the database connection
#     db = get_db()
#     # Delete ALL user documents and return the result
#     db.users.delete_many({})

