# JSON API for meal plan CRUD operations.
# A meal plan belongs to one user and contains an embedded array of daily entries,
# each with a recipe reference and optional notes.
from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId

meal_plans_bp = Blueprint("meal_plans", __name__)


def _serialize(plan):
    # Stringify ObjectIds before returning as JSON
    plan["_id"] = str(plan["_id"])
    if "user_id" in plan:
        plan["user_id"] = str(plan["user_id"])
    return plan


# ── GET MEAL PLANS FOR A USER ──
# Returns all plans for one user, sorted by week_start descending (most recent first).
@meal_plans_bp.route("/meal-plans/<user_id>", methods=["GET"])
def get_meal_plans(user_id):
    db = get_db()
    try:
        uid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    plans = list(db.meal_plans.find({"user_id": uid}).sort("week_start", -1))
    return jsonify([_serialize(p) for p in plans]), 200


# ── CREATE MEAL PLAN ──
# days must be a JSON array. MongoDB won't reject a non-list value at insert time,
# but anything iterating over it later would break, so we validate upfront.
@meal_plans_bp.route("/meal-plans", methods=["POST"])
def create_meal_plan():
    db = get_db()
    data = request.get_json()
    required = ["user_id", "week_start", "days"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    try:
        data["user_id"] = ObjectId(data["user_id"])
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    if not isinstance(data["days"], list):
        return jsonify({"error": "days must be an array"}), 400
    result = db.meal_plans.insert_one(data)
    return jsonify({"message": "Meal plan created", "meal_plan_id": str(result.inserted_id)}), 201


# ── UPDATE MEAL PLAN ──
# Only the fields in the allowed list can be changed. _id is excluded so a PUT
# request can't overwrite the document's primary key.
@meal_plans_bp.route("/meal-plans/<plan_id>", methods=["PUT"])
def update_meal_plan(plan_id):
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return jsonify({"error": "Invalid plan_id"}), 400
    data = request.get_json()
    if "user_id" in data:
        try:
            data["user_id"] = ObjectId(data["user_id"])
        except Exception:
            return jsonify({"error": "Invalid user_id"}), 400
    allowed = ["week_start", "days", "notes", "user_id"]
    update_fields = {k: v for k, v in data.items() if k in allowed}
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    result = db.meal_plans.update_one({"_id": oid}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"error": "Meal plan not found"}), 404
    return jsonify({"message": "Meal plan updated successfully", "modified": result.modified_count}), 200


# ── DELETE MEAL PLAN ──
@meal_plans_bp.route("/meal-plans/<plan_id>", methods=["DELETE"])
def delete_meal_plan(plan_id):
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return jsonify({"error": "Invalid plan_id"}), 400
    result = db.meal_plans.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "Meal plan not found"}), 404
    return jsonify({"message": "Meal plan deleted successfully"}), 200
