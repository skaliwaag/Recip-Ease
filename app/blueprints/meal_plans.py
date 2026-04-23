from flask import Blueprint, jsonify, request
from app.db import get_db

# Database setup for meal plans
meal_plans_bp = Blueprint("meal_plans", __name__)

# # Database connection and CRUD operations for meal plans
# def get_db():
#     conn = sqlite3.connect('mealplans.db')
#     conn.row_factory = sqlite3.Row
#     return conn

#------------------------------
# READ/FIND ONE meal plan
#------------------------------
def read_mealplan(mealplan_id: int):
    # Get the database connection
    db = get_db()
    # Find and return the mealplan document by _id
    return db.mealplan.find_one({"_id": mealplan_id})

#------------------------------
# Route for reading one meal plan by ID
#------------------------------
@meal_plans_bp.route("/mealplans/int:mealplan_id>", methods=["GET"])
def read_one_mealplan_route(mealplan_id):
    # Get the mealplan document by ID
    mealplan = meal_plans_bp.read_one_mealplan(mealplan_id)
    # If mealplan not found, return 404 error
    if not mealplan:
        return jsonify({"error": "mealplan not found"}), 404
    # Convert ObjectId to string for JSON serialization
    mealplan["_id"] = str(mealplan["_id"])
    # Return the mealplan document as JSON
    return jsonify(mealplan), 200

#--------------------------------
# READ/FIND ALL mealplans
#--------------------------------
def read_all_mealplans():
    # Get the database connection
    db = get_db()
    # Find and return ALL mealplan documents as a list
    return list(db.mealplan.find())

#--------------------------------
# Route for reading all mealplans
#--------------------------------
@meal_plans_bp.route("/mealplans", methods=["GET"])
def read_all_mealplans_route():
    # Get all mealplans documents
    mealplans = meal_plans_bp.read_all_recipes()
    # Convert ObjectId to string for JSON serialization
    for mealplan in mealplans:
        mealplan["_id"] = str(mealplan["_id"])
    # Return the list of mealplans as JSON
    return jsonify(mealplans), 200

#------------------------------
# CREATE/INSERT meal plan
#------------------------------
def create_mealplan(user_id, week_start, days, notes):
    # Get the database connection
    db = get_db()
    # Create the mealplan document
    mealplans = {
        "user_id": user_id,
        "week_start": week_start,
        "days": days,
        "notes": notes
    }
    # Insert and return the inserted ID
    return db.mealplan.insert_one(mealplans)

#------------------------------
# Route for creating a meal plan
#------------------------------
@meal_plans_bp.route("/mealplans", methods=["POST"])
def create_mealplan_route():
    # Get the JSON data from the request
    data = request.get_json()
    # Retieve the fields from the JSON data
    user_id = data.get("user_id")
    week_start = data.get("week_start")
    days = data.get("days")
    notes = data.get("notes")
    mealplan_id = meal_plans_bp.create_mealplan(user_id, week_start, days, notes)
    # Validate required fields
    if not week_start or not days or not notes:
        return jsonify({"error": "Failed to create meal plan"}), 500
    # Create the meal plan and get the new mealplan ID
    mealplan_id = meal_plans_bp.create_mealplan(user_id, week_start, days, notes)
    # Return a success message with the new mealplan ID
    return jsonify({"message": "Meal plan created", "mealplan_id": str(mealplan_id)}), 201

#------------------------------
# UPDATE ONE meal plan
#------------------------------
def update_mealplan(mealplan_id, user_id, week_start, days, notes):
    # Build the mealplan update
    update_fields = {}
    if user_id:
        update_fields["user_id"] = user_id
    if week_start:
        update_fields["week_start"] = week_start
    if days:
        update_fields["days"] = days
    if notes:
        update_fields["notes"] = notes
    # Get the database connection
    db = get_db()
    # Update the mealplan document by ID and return whether it was successful
    return db.mealplan.update_one(
        {"_id": mealplan_id},
        {"$set": update_fields})
    
#------------------------------
# Route for updating a meal plan by ID
#------------------------------
@meal_plans_bp.route("/mealplans/<int:mealplan_id>", methods=["PUT"])
def update_mealplan_route(mealplan_id):
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve mealplans fields from the JSON data
    week_start = data.get("week_start")
    days = data.get("days")
    notes = data.get("notes")
    # Update the mealplan and get the result
    result = meal_plans_bp.update_mealplan(mealplan_id, week_start, days, notes)
    # If no fields to update, return 400 error
    if result is None:
        return jsonify({"error": "No fields to update"}), 400
    # If mealplan not found, return 404 error
    if not result:
        return jsonify({"error": "Meal plan not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Meal plan updated successfully"}), 200

#------------------------------
# DELETE ONE meal plan
#------------------------------
def delete_mealplan(mealplan_id: int):
    # Get the database connection
    db = get_db()
    # Delete the mealplan document by ID and return whether it was deleted
    result = db.mealplan.delete_one({"_id": mealplan_id})
    # Return the number of documents deleted
    return result.deleted_count

#------------------------------
# Route for deleting a meal plan by ID
#------------------------------
@meal_plans_bp.route("/mealplans/<int:mealplan_id>", methods=["DELETE"])
def delete_mealplan_route(mealplan_id):
    # Delete the mealplan and get the result
    result = meal_plans_bp.delete_mealplan(mealplan_id)
    # If no documents were deleted, return 404 error
    if not result:
        return jsonify({"error": "Meal plan not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Meal plan deleted successfully"}), 200