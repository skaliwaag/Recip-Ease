# JSON API for user CRUD operations.
# Users store dietary preferences and favorite categories, which the
# recommendation engine uses to personalize results.
from flask import Blueprint, jsonify, request
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

users_bp = Blueprint("users", __name__)


def _serialize(user):
    # _id is an ObjectId and can't go into JSON directly
    user["_id"] = str(user["_id"])
    return user


# ── GET ALL USERS ──
# Returns a trimmed view of each user (name, email, preferences, created date).
# Full details including saved recipes and meal plans are at /users/<id>.
@users_bp.route("/users", methods=["GET"])
def get_all_users():
    db = get_db()
    users = list(db.users.find(
        {},
        {"name": 1, "email": 1, "dietary_preferences": 1, "created_at": 1}
    ).sort("name", 1))
    return jsonify([_serialize(u) for u in users]), 200


# ── GET ONE USER ──
@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    user = db.users.find_one({"_id": oid})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(_serialize(user)), 200


# ── CREATE USER ──
# Email must be unique. The users collection has a unique index on that field,
# but we check here first to return a clean 409 instead of a pymongo duplicate key error.
# dietary_preferences and favorite_categories default to empty arrays so the
# recommendation engine always has something to iterate over.
@users_bp.route("/users", methods=["POST"])
def create_user():
    db = get_db()
    data = request.get_json()
    required = ["name", "email"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    if db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already registered"}), 409
    data.setdefault("dietary_preferences", [])
    data.setdefault("favorite_categories", [])
    # Set server-side so the client can't pass in a fake timestamp
    data["created_at"] = datetime.now(timezone.utc)
    result = db.users.insert_one(data)
    return jsonify({"message": "User created successfully", "user_id": str(result.inserted_id)}), 201


# ── UPDATE USER ──
# Only the fields in the allowed list can be changed. _id and created_at are
# excluded intentionally so a PUT request can't overwrite internal fields.
@users_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    data = request.get_json()
    allowed = ["name", "email", "dietary_preferences", "favorite_categories"]
    update_fields = {k: v for k, v in data.items() if k in allowed}
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    result = db.users.update_one({"_id": oid}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated successfully"}), 200


# ── DELETE USER ──
@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400
    result = db.users.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200
