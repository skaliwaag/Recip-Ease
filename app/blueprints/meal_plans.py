# meal_plans.py — routes for creating and managing user meal plans
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.db import get_db
from bson import ObjectId

router = APIRouter()


def _serialize(plan):
    plan["_id"]    = str(plan["_id"])
    plan["userId"] = str(plan["userId"])
    for day in plan.get("days", []):
        day["recipeId"] = str(day["recipeId"])
    return plan


@router.get("/meal-plans/{user_id}")
def get_meal_plans(user_id: str):
    db = get_db()
    try:
        uid = ObjectId(user_id)
    except Exception:
        return JSONResponse({"error": "Invalid user_id"}, status_code=400)

    plans = list(db.mealPlans.find({"userId": uid}).sort("weekStart", -1))
    return [_serialize(p) for p in plans]


@router.post("/meal-plans", status_code=201)
async def create_meal_plan(request: Request):
    db   = get_db()
    data = await request.json()

    required = ["userId", "weekStart", "days"]
    missing  = [f for f in required if f not in data]
    if missing:
        return JSONResponse({"error": f"Missing fields: {missing}"}, status_code=400)

    try:
        data["userId"] = ObjectId(data["userId"])
    except Exception:
        return JSONResponse({"error": "Invalid userId"}, status_code=400)

    if not isinstance(data["days"], list):
        return JSONResponse({"error": "days must be an array"}, status_code=400)

    for day in data["days"]:
        try:
            day["recipeId"] = ObjectId(day["recipeId"])
        except Exception:
            return JSONResponse({"error": "Invalid recipeId in days"}, status_code=400)

    result = db.mealPlans.insert_one(data)
    return JSONResponse({"inserted_id": str(result.inserted_id)}, status_code=201)


@router.put("/meal-plans/{plan_id}")
async def update_meal_plan(plan_id: str, request: Request):
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return JSONResponse({"error": "Invalid plan_id"}, status_code=400)

    data = await request.json()

    if "userId" in data:
        try:
            data["userId"] = ObjectId(data["userId"])
        except Exception:
            return JSONResponse({"error": "Invalid userId"}, status_code=400)

    if "days" in data:
        if not isinstance(data["days"], list):
            return JSONResponse({"error": "days must be an array"}, status_code=400)
        for day in data["days"]:
            try:
                day["recipeId"] = ObjectId(day["recipeId"])
            except Exception:
                return JSONResponse({"error": "Invalid recipeId in days"}, status_code=400)

    result = db.mealPlans.update_one({"_id": oid}, {"$set": data})
    if result.matched_count == 0:
        return JSONResponse({"error": "Meal plan not found"}, status_code=404)
    return {"modified": result.modified_count}


@router.delete("/meal-plans/{plan_id}")
def delete_meal_plan(plan_id: str):
    db = get_db()
    try:
        oid = ObjectId(plan_id)
    except Exception:
        return JSONResponse({"error": "Invalid plan_id"}, status_code=400)

    result = db.mealPlans.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return JSONResponse({"error": "Meal plan not found"}, status_code=404)
    return {"deleted": result.deleted_count}
