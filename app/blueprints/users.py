from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

users_bp = Blueprint("users", __name__)


def _serialize(doc):
    doc["_id"] = str(doc["_id"])
    doc["favoriteCategories"] = [str(c) for c in doc.get("favoriteCategories", [])]
    return doc


@users_bp.route("/users")
def user_list():
    db    = get_db()
    users = list(db.users.find({}, {"dietaryPreferences": 1, "name": 1, "email": 1, "createdAt": 1}).sort("name", 1))
    return jsonify([_serialize(u) for u in users])


@users_bp.route("/users/<user_id>")
def user_detail(user_id):
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400

    user = db.users.find_one({"_id": oid})
    if not user:
        return jsonify({"error": "User not found"}), 404

    saved = list(db.savedRecipes.aggregate([
        {"$match": {"userId": oid}},
        {"$lookup": {"from": "recipes", "localField": "recipeId", "foreignField": "_id", "as": "recipe"}},
        {"$unwind": "$recipe"},
        {"$project": {"_id": {"$toString": "$recipe._id"}, "title": "$recipe.title", "submissionDateTime": 1}}
    ]))

    meal_plans = list(db.mealPlans.find({"userId": oid}).sort("weekStart", -1))
    for plan in meal_plans:
        plan["_id"]    = str(plan["_id"])
        plan["userId"] = str(plan["userId"])
        for day in plan.get("days", []):
            day["recipeId"] = str(day["recipeId"])

    user = _serialize(user)
    user["savedRecipes"] = saved
    user["mealPlans"]    = meal_plans
    return jsonify(user)


@users_bp.route("/users", methods=["POST"])
def create_user():
    db   = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["name", "email"]
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    if db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already registered"}), 409

    data.setdefault("dietaryPreferences", [])
    data.setdefault("favoriteCategories", [])
    data["createdAt"] = datetime.now(timezone.utc)
    result = db.users.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201
