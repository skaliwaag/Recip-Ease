from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

meal_plans_bp = Blueprint("meal_plans", __name__)


def _serialize(plan):
    plan["_id"]    = str(plan["_id"])
    plan["userId"] = str(plan["userId"])
    for day in plan.get("days", []):
        day["recipeId"] = str(day["recipeId"])
    return plan


@meal_plans_bp.route("/meal-plans/<user_id>")
def get_meal_plans(user_id):
    db = get_db()
    try:
        uid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400

    plans = list(db.mealPlans.find({"userId": uid}).sort("weekStart", -1))
    return jsonify([_serialize(p) for p in plans])


@meal_plans_bp.route("/meal-plans", methods=["POST"])
def create_meal_plan():
    db   = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["userId", "weekStart", "days"]
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        data["userId"] = ObjectId(data["userId"])
    except Exception:
        return jsonify({"error": "Invalid userId"}), 400

    if not isinstance(data["days"], list):
        return jsonify({"error": "days must be an array"}), 400

    for day in data["days"]:
        try:
            day["recipeId"] = ObjectId(day["recipeId"])
        except Exception:
            return jsonify({"error": "Invalid recipeId in days"}), 400

    result = db.mealPlans.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


@meal_plans_bp.route("/meal-plans/<plan_id>", methods=["PUT"])
def update_meal_plan(plan_id):
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return jsonify({"error": "Invalid plan_id"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "userId" in data:
        try:
            data["userId"] = ObjectId(data["userId"])
        except Exception:
            return jsonify({"error": "Invalid userId"}), 400

    if "days" in data:
        if not isinstance(data["days"], list):
            return jsonify({"error": "days must be an array"}), 400
        for day in data["days"]:
            try:
                day["recipeId"] = ObjectId(day["recipeId"])
            except Exception:
                return jsonify({"error": "Invalid recipeId in days"}), 400

    result = db.mealPlans.update_one({"_id": oid}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Meal plan not found"}), 404
    return jsonify({"modified": result.modified_count})


@meal_plans_bp.route("/meal-plans/<plan_id>", methods=["DELETE"])
def delete_meal_plan(plan_id):
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return jsonify({"error": "Invalid plan_id"}), 400

    result = db.mealPlans.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "Meal plan not found"}), 404
    return jsonify({"deleted": result.deleted_count})
