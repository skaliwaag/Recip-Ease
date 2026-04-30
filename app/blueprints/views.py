from flask import render_template, redirect, url_for, request, flash
from app.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

# these have to match exactly what's stored in mongo — changing them here without
# updating the db too will silently break the dietary filter
DIETARY_FLAGS = ["vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free"]


def register_routes(app):

    @app.route("/")
    def index():
        db = get_db()
        q        = request.args.get("q", "").strip()
        flag     = request.args.get("flag", "").strip()
        category = request.args.get("category", "").strip()

        query = {}
        if q:
            # $text only works if the text index exists in Atlas — run create_indexes.py first
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

        return render_template("index.html",
            recipes=recipes,
            categories=categories,
            dietary_flags=DIETARY_FLAGS,
            q=q, flag=flag, category=category)


    @app.route("/recipe/new", methods=["GET"])
    def recipe_new():
        db = get_db()
        categories = list(db.categories.find({}).sort("name", 1))
        for c in categories:
            c["_id"] = str(c["_id"])
        users = list(db.users.find({}, {"name": 1}).sort("name", 1))
        for u in users:
            u["_id"] = str(u["_id"])
        return render_template("recipe_form.html",
            categories=categories,
            users=users,
            dietary_flags=DIETARY_FLAGS)


    @app.route("/recipe/new", methods=["POST"])
    def recipe_new_post():
        db = get_db()
        try:
            category_oid = ObjectId(request.form["categoryId"])
            author_oid   = ObjectId(request.form["authorUserId"])
        except Exception:
            flash("Invalid category or author selection.", "danger")
            return redirect(url_for("recipe_new"))

        tags          = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
        dietary_flags = request.form.getlist("dietaryFlags")

        db.recipes.insert_one({
            "title":       request.form["title"],
            "description": request.form["description"],
            "categoryId":  category_oid,
            "authorUserId": author_oid,
            # form sends one ingredient per line, wrapping in dicts to match how the seed stores them
            "ingredients": [{"name": i.strip()} for i in request.form.get("ingredients", "").split("\n") if i.strip()],
            "prepTime":    int(request.form.get("prepTime", 0)),
            "cookTime":    int(request.form.get("cookTime", 0)),
            "servings":    int(request.form.get("servings", 1)),
            "tags":        tags,
            "dietaryFlags": dietary_flags,
        })
        flash("Recipe added!", "success")
        return redirect(url_for("index"))


    @app.route("/recipe/<recipe_id>")
    def recipe_detail(recipe_id):
        db = get_db()
        try:
            oid = ObjectId(recipe_id)
        except Exception:
            return "Invalid recipe ID", 400

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
            return "Recipe not found", 404

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

        return render_template("recipe_detail.html", recipe=recipe, users=users)


    @app.route("/recipe/<recipe_id>/delete", methods=["POST"])
    def recipe_delete(recipe_id):
        db = get_db()
        try:
            db.recipes.delete_one({"_id": ObjectId(recipe_id)})
        except Exception:
            pass  # bad id shouldn't crash the page, just go back to home
        return redirect(url_for("index"))


    @app.route("/recipe/<recipe_id>/review", methods=["POST"])
    def review_create(recipe_id):
        db = get_db()
        try:
            recipe_oid = ObjectId(recipe_id)
            user_oid   = ObjectId(request.form["userId"])
            rating     = int(request.form["rating"])
        except Exception:
            flash("Invalid review data.", "danger")
            return redirect(url_for("recipe_detail", recipe_id=recipe_id))

        if not 1 <= rating <= 5:
            flash("Rating must be between 1 and 5.", "danger")
            return redirect(url_for("recipe_detail", recipe_id=recipe_id))

        db.reviews.insert_one({
            "recipeId":       recipe_oid,
            "userId":         user_oid,
            "rating":         rating,
            "comment":        request.form.get("comment", ""),
            "reviewDateTime": datetime.now(timezone.utc),
        })
        return redirect(url_for("recipe_detail", recipe_id=recipe_id))


    @app.route("/recommendations")
    def recommendations():
        db = get_db()
        users = list(db.users.find({}, {"name": 1}).sort("name", 1))
        for u in users:
            u["_id"] = str(u["_id"])

        user_id = request.args.get("user_id", "").strip()
        selected_user = None
        results = []

        if user_id:
            try:
                user = db.users.find_one({"_id": ObjectId(user_id)})
            except Exception:
                user = None

            if user:
                selected_user = {"_id": user_id, "name": user["name"]}
                dietary_prefs  = user.get("dietaryPreferences", [])
                fav_categories = user.get("favoriteCategories", [])

                conditions = []
                if dietary_prefs:
                    conditions.append({"dietaryFlags": {"$in": dietary_prefs}})
                if fav_categories:
                    conditions.append({"categoryId": {"$in": fav_categories}})
                match_filter = {"$or": conditions} if conditions else {}

                pipeline = [
                    {"$match": match_filter},
                    {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "recipeId", "as": "reviews"}},
                    {"$addFields": {"avgRating": {"$avg": "$reviews.rating"}, "reviewCount": {"$size": "$reviews"}}},
                    {"$sort": {"avgRating": -1}},
                    {"$limit": 3},
                ]
                results = list(db.recipes.aggregate(pipeline))
                for r in results:
                    r["_id"] = str(r["_id"])

        return render_template("recommendations.html",
            users=users,
            selected_user=selected_user,
            results=results,
            user_id=user_id)


    @app.route("/review/<review_id>/delete", methods=["POST"])
    def review_delete(review_id):
        recipe_id = request.form.get("recipe_id", "")
        db = get_db()
        try:
            db.reviews.delete_one({"_id": ObjectId(review_id)})
        except Exception:
            pass
        return redirect(url_for("recipe_detail", recipe_id=recipe_id))
