from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime

recipes_bp = Blueprint("recipes", __name__)


def _serialize(doc):
    doc["_id"] = str(doc["_id"])
    if "categoryId" in doc:
        doc["categoryId"] = str(doc["categoryId"])
    if "authorUserId" in doc:
        doc["authorUserId"] = str(doc["authorUserId"])
    return doc


@recipes_bp.route("/recipes")
def recipe_list():
    db = get_db()
    q        = request.args.get("q", "").strip()
    flag     = request.args.get("flag", "").strip()
    category = request.args.get("category", "").strip()

    query = {}
    if q:
        query["$text"] = {"$search": q}
    if flag:
        query["dietaryFlags"] = flag
    if category:
        try:
            query["categoryId"] = ObjectId(category)
        except Exception:
            return jsonify({"error": "Invalid category id"}), 400

    recipes = list(db.recipes.find(query).sort("title", 1))
    return jsonify([_serialize(r) for r in recipes])


@recipes_bp.route("/recipes/<recipe_id>")
def recipe_detail(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400

    pipeline = [
        {"$match": {"_id": oid}},
        {"$lookup": {"from": "categories", "localField": "categoryId",   "foreignField": "_id", "as": "category"}},
        {"$lookup": {"from": "users",      "localField": "authorUserId", "foreignField": "_id", "as": "author"}},
        {"$lookup": {"from": "reviews",    "localField": "_id",          "foreignField": "recipeId", "as": "reviews"}},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$author",   "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}}},
    ]
    results = list(db.recipes.aggregate(pipeline))
    if not results:
        return jsonify({"error": "Recipe not found"}), 404

    doc = results[0]
    doc["_id"]          = str(doc["_id"])
    doc["categoryId"]   = str(doc.get("categoryId", ""))
    doc["authorUserId"] = str(doc.get("authorUserId", ""))
    if "category" in doc:
        doc["category"]["_id"] = str(doc["category"]["_id"])
    if "author" in doc:
        doc["author"]["_id"] = str(doc["author"]["_id"])
    for r in doc.get("reviews", []):
        r["_id"]      = str(r["_id"])
        r["userId"]   = str(r["userId"])
        r["recipeId"] = str(r["recipeId"])
    return jsonify(doc)


@recipes_bp.route("/recipes", methods=["POST"])
def create_recipe():
    db   = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["title", "description", "categoryId", "authorUserId", "ingredients", "prepTime", "cookTime", "servings"]
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        data["categoryId"]   = ObjectId(data["categoryId"])
        data["authorUserId"] = ObjectId(data["authorUserId"])
    except Exception:
        return jsonify({"error": "Invalid categoryId or authorUserId"}), 400

    data.setdefault("tags", [])
    data.setdefault("dietaryFlags", [])
    result = db.recipes.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


@recipes_bp.route("/recipes/<recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe_id"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    for field in ["categoryId", "authorUserId"]:
        if field in data:
            try:
                data[field] = ObjectId(data[field])
            except Exception:
                return jsonify({"error": f"Invalid {field}"}), 400

    result = db.recipes.update_one({"_id": oid}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify({"modified": result.modified_count})


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
    return jsonify({"deleted": result.deleted_count})
