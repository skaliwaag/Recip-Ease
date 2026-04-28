from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId

# Database setup for meal plans
meal_plans_bp = Blueprint("meal_plans", __name__)


def _serialize(plan):
    # Convert ObjectId to string for JSON serialization
    plan["_id"] = str(plan["_id"])
    if "user_id" in plan:
        plan["user_id"] = str(plan["user_id"])
    return plan


#--------------------------------
# READ/FIND ALL mealplans
#--------------------------------
@meal_plans_bp.route("/meal-plans/<user_id>", methods=["GET"])
def get_meal_plans(user_id):
    # Get the database connection
    db = get_db()
    try:
        uid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    # Get all mealplans documents
    plans = list(db.meal_plans.find({"user_id": uid}).sort("week_start", -1))
    # Return the list of mealplans as JSON
    return jsonify([_serialize(p) for p in plans]), 200


#------------------------------
# CREATE/INSERT meal plan
#------------------------------
@meal_plans_bp.route("/meal-plans", methods=["POST"])
def create_meal_plan():
    # Get the database connection
    db = get_db()
    # Get the JSON data from the request
    data = request.get_json()
    # Retieve the fields from the JSON data
    required = ["user_id", "week_start", "days"]
    missing = [f for f in required if f not in data]
    # Validate required fields
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    try:
        data["user_id"] = ObjectId(data["user_id"])
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    if not isinstance(data["days"], list):
        return jsonify({"error": "days must be an array"}), 400
    # Create the meal plan and get the new mealplan ID
    result = db.meal_plans.insert_one(data)
    # Return a success message with the new mealplan ID
    return jsonify({"message": "Meal plan created", "meal_plan_id": str(result.inserted_id)}), 201


#------------------------------
# UPDATE ONE meal plan
#------------------------------
@meal_plans_bp.route("/meal-plans/<plan_id>", methods=["PUT"])
def update_meal_plan(plan_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return jsonify({"error": "Invalid plan_id"}), 400
    # Get the JSON data from the request
    data = request.get_json()
    if "user_id" in data:
        try:
            data["user_id"] = ObjectId(data["user_id"])
        except Exception:
            return jsonify({"error": "Invalid user_id"}), 400
    # Build the mealplan update
    allowed = ["week_start", "days", "notes", "user_id"]
    # ensures that only fields with values are updated
    update_fields = {k: v for k, v in data.items() if k in allowed}
    # If no fields to update, return 400 error
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    # Update the mealplan document by ID and return whether it was successful
    result = db.meal_plans.update_one({"_id": oid}, {"$set": update_fields})
    # If mealplan not found, return 404 error
    if result.matched_count == 0:
        return jsonify({"error": "Meal plan not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Meal plan updated successfully", "modified": result.modified_count}), 200


#------------------------------
# DELETE ONE meal plan
#------------------------------
@meal_plans_bp.route("/meal-plans/<plan_id>", methods=["DELETE"])
def delete_meal_plan(plan_id):
    # Get the database connection
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return jsonify({"error": "Invalid plan_id"}), 400
    # Delete the mealplan document by ID and return whether it was deleted
    result = db.meal_plans.delete_one({"_id": oid})
    # If no documents were deleted, return 404 error
    if result.deleted_count == 0:
        return jsonify({"error": "Meal plan not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Meal plan deleted successfully"}), 200
