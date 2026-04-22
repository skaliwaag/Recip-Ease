# users.py — CRUD routes for user accounts (register, profile, preferences)
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()


def _serialize(doc):
    doc["_id"] = str(doc["_id"])
    doc["favoriteCategories"] = [str(c) for c in doc.get("favoriteCategories", [])]
    return doc


@router.get("/users")
def user_list():
    db    = get_db()
    users = list(db.users.find({}, {"dietaryPreferences": 1, "name": 1, "email": 1, "createdAt": 1}).sort("name", 1))
    return [_serialize(u) for u in users]


@router.get("/users/{user_id}")
def user_detail(user_id: str):
    db = get_db()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return JSONResponse({"error": "Invalid user_id"}, status_code=400)

    user = db.users.find_one({"_id": oid})
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

    saved = list(db.savedRecipes.aggregate([
        {"$match": {"userId": oid}},
        {"$lookup": {"from": "recipes", "localField": "recipeId", "foreignField": "_id", "as": "recipe"}},
        {"$unwind": "$recipe"},
        {"$project": {"_id": {"$toString": "$recipe._id"}, "title": "$recipe.title", "submissionDateTime": 1}},
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
    return user


@router.post("/users", status_code=201)
async def create_user(request: Request):
    db   = get_db()
    data = await request.json()

    required = ["name", "email"]
    missing  = [f for f in required if f not in data]
    if missing:
        return JSONResponse({"error": f"Missing fields: {missing}"}, status_code=400)

    if db.users.find_one({"email": data["email"]}):
        return JSONResponse({"error": "Email already registered"}, status_code=409)

    data.setdefault("dietaryPreferences", [])
    data.setdefault("favoriteCategories", [])
    data["createdAt"] = datetime.now(timezone.utc)
    result = db.users.insert_one(data)
    return JSONResponse({"inserted_id": str(result.inserted_id)}, status_code=201)
