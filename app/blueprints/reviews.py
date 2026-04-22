# reviews.py — API routes for recipe reviews (create, delete)
# HTML review routes (POST from recipe detail page) are handled in views.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()


@router.get("/reviews/{recipe_id}")
def get_reviews(recipe_id: str):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return JSONResponse({"error": "Invalid recipe_id"}, status_code=400)

    reviews = list(db.reviews.find({"recipeId": oid}).sort("reviewDateTime", -1))
    for r in reviews:
        r["_id"]      = str(r["_id"])
        r["userId"]   = str(r["userId"])
        r["recipeId"] = str(r["recipeId"])
    return reviews


@router.post("/reviews", status_code=201)
async def create_review(request: Request):
    db   = get_db()
    data = await request.json()

    required = ["userId", "recipeId", "rating"]
    missing  = [f for f in required if f not in data]
    if missing:
        return JSONResponse({"error": f"Missing fields: {missing}"}, status_code=400)

    try:
        data["userId"]   = ObjectId(data["userId"])
        data["recipeId"] = ObjectId(data["recipeId"])
    except Exception:
        return JSONResponse({"error": "Invalid userId or recipeId"}, status_code=400)

    if not isinstance(data["rating"], int) or not 1 <= data["rating"] <= 5:
        return JSONResponse({"error": "rating must be an integer 1–5"}, status_code=400)

    data.setdefault("comment", "")
    data["reviewDateTime"] = datetime.now(timezone.utc)
    result = db.reviews.insert_one(data)
    return JSONResponse({"inserted_id": str(result.inserted_id)}, status_code=201)


@router.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    db = get_db()
    try:
        oid = ObjectId(review_id)
    except Exception:
        return JSONResponse({"error": "Invalid review_id"}, status_code=400)

    result = db.reviews.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return JSONResponse({"error": "Review not found"}, status_code=404)
    return {"deleted": result.deleted_count}
