# JSON API for recipe CRUD operations.
# All routes return JSON. ObjectIds are serialized to strings before returning
# because the bson.ObjectId type is not directly JSON-serializable.
from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId

recipes_bp = Blueprint("recipes", __name__)


def _serialize(recipe):
    # MongoDB stores _id, category_id, and author_user_id as ObjectId objects.
    # jsonify can't handle those directly, so we convert them to strings here
    # before the response goes out.
    recipe["_id"] = str(recipe["_id"])
    if "category_id" in recipe:
        recipe["category_id"] = str(recipe["category_id"])
    if "author_user_id" in recipe:
        recipe["author_user_id"] = str(recipe["author_user_id"])
    return recipe


# ── GET ALL RECIPES ──
# Returns every recipe sorted alphabetically by title.
@recipes_bp.route("/recipes", methods=["GET"])
def get_all_recipes():
    db = get_db()
    recipes = list(db.recipes.find().sort("title", 1))
    return jsonify([_serialize(r) for r in recipes]), 200


# ── GET ONE RECIPE ──
# Returns a single recipe by its MongoDB _id.
# Returns 400 if the id string is not a valid ObjectId, 404 if no document matches.
@recipes_bp.route("/recipes/<recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    recipe = db.recipes.find_one({"_id": oid})
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify(_serialize(recipe)), 200


# ── CREATE RECIPE ──
# Expects a JSON body with all required fields. category_id and author_user_id
# arrive as plain strings and must be converted to ObjectIds so MongoDB stores
# proper references instead of raw strings.
@recipes_bp.route("/recipes", methods=["POST"])
def create_recipe():
    db = get_db()
    data = request.get_json()
    required = ["title", "description", "category_id", "author_user_id", "ingredients", "prep_time", "cook_time", "servings"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    try:
        data["category_id"] = ObjectId(data["category_id"])
        data["author_user_id"] = ObjectId(data["author_user_id"])
    except Exception:
        return jsonify({"error": "Invalid category_id or author_user_id"}), 400
    # Default to empty arrays so recipes without tags or flags don't break
    # any $in filter queries that iterate over those fields.
    data.setdefault("tags", [])
    data.setdefault("dietary_flags", [])
    result = db.recipes.insert_one(data)
    return jsonify({"message": "Recipe created", "recipe_id": str(result.inserted_id)}), 201


# ── UPDATE RECIPE ──
# Partial update via $set, so only the fields included in the request body change.
# Returns 404 if no document with that _id exists.
@recipes_bp.route("/recipes/<recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    data = request.get_json()
    # Convert reference fields to ObjectId if they're being updated
    for field in ["category_id", "author_user_id"]:
        if field in data:
            try:
                data[field] = ObjectId(data[field])
            except Exception:
                return jsonify({"error": f"Invalid {field}"}), 400
    result = db.recipes.update_one({"_id": oid}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify({"message": "Recipe updated successfully", "modified": result.modified_count}), 200


# ── DELETE RECIPE ──
# Hard delete. Returns 404 if the id didn't match any document.
@recipes_bp.route("/recipes/<recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    result = db.recipes.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify({"message": "Recipe deleted successfully"}), 200
