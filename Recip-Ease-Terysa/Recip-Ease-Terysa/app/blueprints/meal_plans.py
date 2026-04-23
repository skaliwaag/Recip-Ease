# fixed: was SQLite-based with no routes; converted to MongoDB (matching the rest of the app)
# and added Flask routes so these functions are actually accessible as API endpoints
from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId

meal_plans_bp = Blueprint("meal_plans", __name__)

#--------------------------------
# CREATE meal plan
#--------------------------------
def create_mealplan(user_id, week_start, days, notes):
    db = get_db()
    mealplan = {
        "user_id": user_id,
        "week_start": week_start,
        "days": days,
        "notes": notes
    }
    return db.meal_plans.insert_one(mealplan).inserted_id

#--------------------------------
# Route for creating a meal plan
#--------------------------------
@meal_plans_bp.route("/meal_plans", methods=["POST"])
def create_mealplan_route():
    data = request.get_json()
    user_id = data.get("user_id")
    week_start = data.get("week_start")
    days = data.get("days")
    notes = data.get("notes")
    if not user_id or not week_start:
        return jsonify({"error": "Missing required fields"}), 400
    mealplan_id = create_mealplan(user_id, week_start, days, notes)
    return jsonify({"message": "Meal plan created", "mealplan_id": str(mealplan_id)}), 201

#--------------------------------
# READ ONE meal plan by ID
#--------------------------------
def read_mealplan(mealplan_id):
    db = get_db()
    # fixed: MongoDB uses ObjectId for _id, not a plain int like SQLite
    return db.meal_plans.find_one({"_id": ObjectId(mealplan_id)})

#--------------------------------
# Route for reading a meal plan by ID
#--------------------------------
@meal_plans_bp.route("/meal_plans/<mealplan_id>", methods=["GET"])
def read_mealplan_route(mealplan_id):
    mealplan = read_mealplan(mealplan_id)
    if not mealplan:
        return jsonify({"error": "Meal plan not found"}), 404
    mealplan["_id"] = str(mealplan["_id"])
    return jsonify(mealplan), 200

#--------------------------------
# UPDATE meal plan
#--------------------------------
def update_mealplan(mealplan_id, user_id, week_start, days, notes):
    update_fields = {}
    if user_id is not None:
        update_fields["user_id"] = user_id
    if week_start is not None:
        update_fields["week_start"] = week_start
    if days is not None:
        update_fields["days"] = days
    if notes is not None:
        update_fields["notes"] = notes
    if not update_fields:
        return None
    db = get_db()
    return db.meal_plans.update_one({"_id": ObjectId(mealplan_id)}, {"$set": update_fields})

#--------------------------------
# Route for updating a meal plan by ID
#--------------------------------
@meal_plans_bp.route("/meal_plans/<mealplan_id>", methods=["PUT"])
def update_mealplan_route(mealplan_id):
    data = request.get_json()
    user_id = data.get("user_id")
    week_start = data.get("week_start")
    days = data.get("days")
    notes = data.get("notes")
    result = update_mealplan(mealplan_id, user_id, week_start, days, notes)
    if result is None:
        return jsonify({"error": "No fields to update"}), 400
    if result.modified_count == 0:
        return jsonify({"error": "Meal plan not found or no changes made"}), 404
    return jsonify({"message": "Meal plan updated successfully"}), 200

#--------------------------------
# DELETE meal plan
#--------------------------------
def delete_mealplan(mealplan_id):
    db = get_db()
    return db.meal_plans.delete_one({"_id": ObjectId(mealplan_id)})

#--------------------------------
# Route for deleting a meal plan by ID
#--------------------------------
@meal_plans_bp.route("/meal_plans/<mealplan_id>", methods=["DELETE"])
def delete_mealplan_route(mealplan_id):
    result = delete_mealplan(mealplan_id)
    if result.deleted_count == 0:
        return jsonify({"error": "Meal plan not found"}), 404
    return jsonify({"message": "Meal plan deleted successfully"}), 200
