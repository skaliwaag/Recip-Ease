from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

DIETARY_FLAGS = ["vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free"]


def flash(request: Request, message: str, category: str = "info"):
    if "flash_messages" not in request.session:
        request.session["flash_messages"] = []
    request.session["flash_messages"].append([category, message])


def pop_flash(request: Request):
    return request.session.pop("flash_messages", [])


@router.get("/", response_class=HTMLResponse)
def index(request: Request, q: str = "", flag: str = "", category: str = ""):
    db = get_db()
    q = q.strip()
    flag = flag.strip()
    category = category.strip()

    query = {}
    if q:
        query["$text"] = {"$search": q}
    if flag:
        query["dietaryFlags"] = flag
    if category:
        try:
            query["categoryId"] = ObjectId(category)
        except Exception:
            pass

    recipes = list(db.recipes.find(query).sort("title", 1))
    for r in recipes:
        r["_id"] = str(r["_id"])

    categories = list(db.categories.find({}).sort("name", 1))
    for c in categories:
        c["_id"] = str(c["_id"])

    return templates.TemplateResponse(request=request, name="index.html", context={
        "recipes": recipes,
        "categories": categories,
        "dietary_flags": DIETARY_FLAGS,
        "q": q,
        "flag": flag,
        "category": category,
        "flash_messages": pop_flash(request),
    })


@router.get("/recipe/new", response_class=HTMLResponse)
def recipe_new(request: Request):
    db = get_db()
    categories = list(db.categories.find({}).sort("name", 1))
    for c in categories:
        c["_id"] = str(c["_id"])

    users = list(db.users.find({}, {"name": 1}).sort("name", 1))
    for u in users:
        u["_id"] = str(u["_id"])

    return templates.TemplateResponse(request=request, name="recipe_form.html", context={
        "categories": categories,
        "users": users,
        "dietary_flags": DIETARY_FLAGS,
        "flash_messages": pop_flash(request),
    })


@router.post("/recipe/new")
async def recipe_new_post(request: Request):
    db = get_db()
    form = await request.form()
    try:
        category_oid = ObjectId(form["categoryId"])
        author_oid = ObjectId(form["authorUserId"])
    except Exception:
        flash(request, "Invalid category or author selection.", "danger")
        return RedirectResponse("/recipe/new", status_code=303)

    tags = [t.strip() for t in form.get("tags", "").split(",") if t.strip()]
    dietary_flags = form.getlist("dietaryFlags")

    db.recipes.insert_one({
        "title": form["title"],
        "description": form["description"],
        "categoryId": category_oid,
        "authorUserId": author_oid,
        "ingredients": [{"name": i.strip()} for i in form.get("ingredients", "").split("\n") if i.strip()],
        "prepTime": int(form.get("prepTime", 0)),
        "cookTime": int(form.get("cookTime", 0)),
        "servings": int(form.get("servings", 1)),
        "tags": tags,
        "dietaryFlags": dietary_flags,
    })
    return RedirectResponse("/", status_code=303)


@router.get("/recipe/{recipe_id}", response_class=HTMLResponse)
def recipe_detail(recipe_id: str, request: Request):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return Response(content="Invalid recipe ID", status_code=400)

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
        return Response(content="Recipe not found", status_code=404)

    recipe = results[0]
    recipe["_id"]          = str(recipe["_id"])
    recipe["categoryId"]   = str(recipe.get("categoryId", ""))
    recipe["authorUserId"] = str(recipe.get("authorUserId", ""))
    if "category" in recipe:
        recipe["category"]["_id"] = str(recipe["category"]["_id"])
    if "author" in recipe:
        recipe["author"]["_id"] = str(recipe["author"]["_id"])
    for r in recipe.get("reviews", []):
        r["_id"]      = str(r["_id"])
        r["userId"]   = str(r["userId"])
        r["recipeId"] = str(r["recipeId"])

    users = list(db.users.find({}, {"name": 1}).sort("name", 1))
    for u in users:
        u["_id"] = str(u["_id"])

    return templates.TemplateResponse(request=request, name="recipe_detail.html", context={
        "recipe": recipe,
        "users": users,
        "flash_messages": pop_flash(request),
    })


@router.post("/recipe/{recipe_id}/delete")
def recipe_delete(recipe_id: str, request: Request):
    db = get_db()
    try:
        oid = ObjectId(recipe_id)
    except Exception:
        return Response(content="Invalid recipe ID", status_code=400)
    db.recipes.delete_one({"_id": oid})
    return RedirectResponse("/", status_code=303)


@router.post("/recipe/{recipe_id}/review")
async def review_create(recipe_id: str, request: Request):
    db = get_db()
    form = await request.form()
    try:
        recipe_oid = ObjectId(recipe_id)
        user_oid   = ObjectId(form["userId"])
        rating     = int(form["rating"])
    except Exception:
        flash(request, "Invalid review data.", "danger")
        return RedirectResponse(f"/recipe/{recipe_id}", status_code=303)

    if not 1 <= rating <= 5:
        flash(request, "Rating must be between 1 and 5.", "danger")
        return RedirectResponse(f"/recipe/{recipe_id}", status_code=303)

    db.reviews.insert_one({
        "recipeId":       recipe_oid,
        "userId":         user_oid,
        "rating":         rating,
        "comment":        form.get("comment", ""),
        "reviewDateTime": datetime.now(timezone.utc),
    })
    return RedirectResponse(f"/recipe/{recipe_id}", status_code=303)


@router.post("/review/{review_id}/delete")
async def review_delete(review_id: str, request: Request):
    db = get_db()
    form = await request.form()
    recipe_id = form.get("recipe_id", "")
    try:
        db.reviews.delete_one({"_id": ObjectId(review_id)})
    except Exception:
        pass
    return RedirectResponse(f"/recipe/{recipe_id}", status_code=303)


@router.get("/stats", response_class=HTMLResponse)
def stats(request: Request):
    db = get_db()

    recipes_per_category = list(db.recipes.aggregate([
        {"$lookup": {"from": "categories", "localField": "categoryId", "foreignField": "_id", "as": "category"}},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$categoryId", "name": {"$first": "$category.name"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]))
    for d in recipes_per_category:
        d["_id"] = str(d["_id"])

    top_rated = list(db.recipes.aggregate([
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "recipeId", "as": "reviews"}},
        {"$match": {"reviews.0": {"$exists": True}}},
        {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}, "reviewCount": {"$size": "$reviews"}}},
        {"$project": {"title": 1, "avgRating": 1, "reviewCount": 1}},
        {"$sort": {"avgRating": -1}},
        {"$limit": 5},
    ]))
    for d in top_rated:
        d["_id"] = str(d["_id"])

    most_saved = list(db.savedRecipes.aggregate([
        {"$group": {"_id": "$recipeId", "saveCount": {"$sum": 1}}},
        {"$lookup": {"from": "recipes", "localField": "_id", "foreignField": "_id", "as": "recipe"}},
        {"$unwind": "$recipe"},
        {"$project": {"title": "$recipe.title", "saveCount": 1}},
        {"$sort": {"saveCount": -1}},
        {"$limit": 5},
    ]))
    for d in most_saved:
        d["_id"] = str(d["_id"])

    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "recipes_per_category": recipes_per_category,
        "top_rated": top_rated,
        "most_saved": most_saved,
        "flash_messages": pop_flash(request),
    })
