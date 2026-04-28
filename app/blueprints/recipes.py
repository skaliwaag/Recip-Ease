from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId

# Blueprint for recipes
recipes_bp = Blueprint("recipes", __name__)


def _serialize(recipe):
    # Convert ObjectId to string for JSON serialization
    recipe["_id"] = str(recipe["_id"])
    if "category_id" in recipe:
        recipe["category_id"] = str(recipe["category_id"])
    if "author_user_id" in recipe:
        recipe["author_user_id"] = str(recipe["author_user_id"])
    return recipe


#--------------------------------
# READ/FIND ALL recipes
#--------------------------------
@recipes_bp.route("/recipes", methods=["GET"])
def get_all_recipes():
    # Get the database connection
    db = get_db()
    # Get all recipe documents
    recipes = list(db.recipes.find().sort("title", 1))
    # Return the list of recipes as JSON
    return jsonify([_serialize(r) for r in recipes]), 200


#-------------------------------------
# READ/FIND ONE recipe by ID
#-------------------------------------
@recipes_bp.route("/recipes/<recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    # Find and return the recipe document by _id
    recipe = db.recipes.find_one({"_id": oid})
    # If recipe not found, return 404 error
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    # Return the recipe document as JSON
    return jsonify(_serialize(recipe)), 200


#--------------------------------
# CREATE/INSERT recipe
#--------------------------------
@recipes_bp.route("/recipes", methods=["POST"])
def create_recipe():
    # Get the database connection
    db = get_db()
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve recipe fields from the JSON data
    required = ["title", "description", "category_id", "author_user_id", "ingredients", "prep_time", "cook_time", "servings"]
    missing = [f for f in required if f not in data]
    # Validate required fields
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    try:
        data["category_id"] = ObjectId(data["category_id"])
        data["author_user_id"] = ObjectId(data["author_user_id"])
    except Exception:
        return jsonify({"error": "Invalid category_id or author_user_id"}), 400
    data.setdefault("tags", [])
    data.setdefault("dietary_flags", [])
    # Create the recipe and get the new recipe ID
    result = db.recipes.insert_one(data)
    # Return a success message with the new recipe ID
    return jsonify({"message": "Recipe created", "recipe_id": str(result.inserted_id)}), 201


#--------------------------------
# UPDATE ONE recipe
#--------------------------------
@recipes_bp.route("/recipes/<recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    # Get the JSON data from the request
    data = request.get_json()
    # Build the recipe update
    for field in ["category_id", "author_user_id"]:
        if field in data:
            try:
                data[field] = ObjectId(data[field])
            except Exception:
                return jsonify({"error": f"Invalid {field}"}), 400
    # Update the recipe document by _id and return whether it was modified
    result = db.recipes.update_one({"_id": oid}, {"$set": data})
    # If no documents were modified, return 404 error
    if result.matched_count == 0:
        return jsonify({"error": "Recipe not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Recipe updated successfully", "modified": result.modified_count}), 200


#--------------------------------
# DELETE ONE recipe
#--------------------------------
@recipes_bp.route("/recipes/<recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    # Delete the recipe document by _id and return whether it was deleted
    result = db.recipes.delete_one({"_id": oid})
    # If no documents were deleted, return 404 error
    if result.deleted_count == 0:
        return jsonify({"error": "Recipe not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Recipe deleted successfully"}), 200
