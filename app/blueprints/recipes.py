# recipes.py — JSON API routes for recipes (list, create, update, delete)
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.db import get_db
from bson import ObjectId

router = APIRouter()


def _serialize(doc):
    doc["_id"] = str(doc["_id"])
    if "categoryId" in doc:
        doc["categoryId"] = str(doc["categoryId"])
    if "authorUserId" in doc:
        doc["authorUserId"] = str(doc["authorUserId"])
    return doc


@router.get("/recipes")
def recipe_list(q: str = "", flag: str = "", category: str = ""):
    db       = get_db()
    q        = q.strip()
    flag     = flag.strip()
    category = category.strip()

    query = {}
    if q:
        # $text search requires the text index from create_indexes.py
        query["$text"] = {"$search": q}
    if flag:
        query["dietaryFlags"] = flag
    if category:
        try:
            query["categoryId"] = ObjectId(category)
        except Exception:
            return JSONResponse({"error": "Invalid category id"}, status_code=400)

    recipes = list(db.recipes.find(query).sort("title", 1))
    return [_serialize(r) for r in recipes]


@router.get("/recipes/{recipe_id}")
def recipe_detail(recipe_id: str):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return JSONResponse({"error": "Invalid recipe_id"}, status_code=400)

    # Single pipeline joins category, author, and reviews and computes avgRating in one query
    pipeline = [
        {"$match": {"_id": oid}},
        {"$lookup": {"from": "categories", "localField": "categoryId",   "foreignField": "_id", "as": "category"}},
        {"$lookup": {"from": "users",      "localField": "authorUserId", "foreignField": "_id", "as": "author"}},
        {"$lookup": {"from": "reviews",    "localField": "_id",          "foreignField": "recipeId", "as": "reviews"}},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$author",   "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}}},
    ]
    results = list(db.recipes.aggregate(pipeline))
    if not results:
        return JSONResponse({"error": "Recipe not found"}, status_code=404)

    doc = results[0]
    doc["_id"]          = str(doc["_id"])
    doc["categoryId"]   = str(doc.get("categoryId", ""))
    doc["authorUserId"] = str(doc.get("authorUserId", ""))
    if "category" in doc:
        doc["category"]["_id"] = str(doc["category"]["_id"])
    if "author" in doc:
        doc["author"]["_id"] = str(doc["author"]["_id"])
    for r in doc.get("reviews", []):
        r["_id"]      = str(r["_id"])
        r["userId"]   = str(r["userId"])
        r["recipeId"] = str(r["recipeId"])
    return doc


@router.post("/recipes", status_code=201)
async def create_recipe(request: Request):
    db   = get_db()
    data = await request.json()

    required = ["title", "description", "categoryId", "authorUserId", "ingredients", "prepTime", "cookTime", "servings"]
    missing  = [f for f in required if f not in data]
    if missing:
        return JSONResponse({"error": f"Missing fields: {missing}"}, status_code=400)

    try:
        data["categoryId"]   = ObjectId(data["categoryId"])
        data["authorUserId"] = ObjectId(data["authorUserId"])
    except Exception:
        return JSONResponse({"error": "Invalid categoryId or authorUserId"}, status_code=400)

    data.setdefault("tags", [])
    data.setdefault("dietaryFlags", [])
    result = db.recipes.insert_one(data)
    return JSONResponse({"inserted_id": str(result.inserted_id)}, status_code=201)


@router.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: str, request: Request):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return JSONResponse({"error": "Invalid recipe_id"}, status_code=400)

    data = await request.json()

    for field in ["categoryId", "authorUserId"]:
        if field in data:
            try:
                data[field] = ObjectId(data[field])
            except Exception:
                return JSONResponse({"error": f"Invalid {field}"}, status_code=400)

    result = db.recipes.update_one({"_id": oid}, {"$set": data})
    if result.matched_count == 0:
        return JSONResponse({"error": "Recipe not found"}, status_code=404)
    return {"modified": result.modified_count}


@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: str):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return JSONResponse({"error": "Invalid recipe_id"}, status_code=400)

    result = db.recipes.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return JSONResponse({"error": "Recipe not found"}, status_code=404)
    return {"deleted": result.deleted_count}
