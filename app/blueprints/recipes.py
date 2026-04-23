from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId

recipes_bp = Blueprint("recipes", __name__)


def _serialize(recipe):
    recipe["_id"] = str(recipe["_id"])
    if "category_id" in recipe:
        recipe["category_id"] = str(recipe["category_id"])
    if "author_user_id" in recipe:
        recipe["author_user_id"] = str(recipe["author_user_id"])
    return recipe


@recipes_bp.route("/recipes", methods=["GET"])
def get_all_recipes():
    db = get_db()
    recipes = list(db.recipes.find().sort("title", 1))
    return jsonify([_serialize(r) for r in recipes]), 200


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
    data.setdefault("tags", [])
    data.setdefault("dietary_flags", [])
    result = db.recipes.insert_one(data)
    return jsonify({"message": "Recipe created", "recipe_id": str(result.inserted_id)}), 201


@recipes_bp.route("/recipes/<recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400
    data = request.get_json()
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
