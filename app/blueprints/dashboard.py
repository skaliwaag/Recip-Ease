from flask import Blueprint, render_template
from app.db import get_db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    db = get_db()

    # ── Pipeline 1: Recipes per category ────────────────────────────────────
    # Goal: count how many recipes belong to each category, sorted by count.
    # Recipes store only a categoryId reference, not the name, so we need a
    # $lookup to resolve the human-readable name before grouping.
    recipes_per_category = list(db.recipes.aggregate([

        # Join categories on categoryId so each recipe document gets an
        # embedded "category" array containing the matching category doc.
        {"$lookup": {
            "from":         "categories",
            "localField":   "categoryId",
            "foreignField": "_id",
            "as":           "category"
        }},

        # Flatten the single-element array into an embedded object.
        # preserveNullAndEmptyArrays keeps recipes whose categoryId is missing
        # or doesn't match any category — without this they'd be silently
        # dropped and the total count would be wrong.
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},

        # Group by categoryId and count recipes in each group.
        # $first picks the category name from the first recipe in the group —
        # all recipes in the group share the same category, so any doc works.
        {"$group": {
            "_id":   "$categoryId",
            "name":  {"$first": "$category.name"},
            "count": {"$sum": 1}
        }},

        # Most-populated categories first
        {"$sort": {"count": -1}},
    ]))
    # ObjectIds aren't JSON-serializable; convert before passing to the template
    for d in recipes_per_category:
        d["_id"] = str(d["_id"])


    # ── Pipeline 2: Top-rated recipes ───────────────────────────────────────
    # Goal: find the 5 highest-rated recipes that have at least one review.
    # Ratings aren't stored on the recipe document — they live in the reviews
    # collection — so we join and compute the average inside the pipeline.
    top_rated = list(db.recipes.aggregate([

        # Join all reviews for each recipe into an embedded array
        {"$lookup": {
            "from":         "reviews",
            "localField":   "_id",
            "foreignField": "recipeId",
            "as":           "reviews"
        }},

        # Drop recipes with no reviews before computing avgRating.
        # Without this filter, $avg on an empty array returns null, and null
        # sorts above real numbers in descending order — so unreviewed recipes
        # would appear at the top of the "top rated" list.
        # reviews.0 checks for the existence of the first array element,
        # which is MongoDB's idiomatic way to test "array is non-empty".
        {"$match": {"reviews.0": {"$exists": True}}},

        # Compute average rating and review count from the joined array
        {"$addFields": {
            "avgRating":   {"$avg":  "$reviews.rating"},
            "reviewCount": {"$size": "$reviews"}
        }},

        # Strip down to only the fields the template needs — avoids sending
        # the full ingredients/tags/etc. arrays across the wire unnecessarily
        {"$project": {"title": 1, "avgRating": 1, "reviewCount": 1}},

        {"$sort":  {"avgRating": -1}},
        {"$limit": 5},
    ]))
    for d in top_rated:
        d["_id"] = str(d["_id"])


    # ── Pipeline 3: Most bookmarked recipes ─────────────────────────────────
    # Goal: find the 5 recipes saved by the most users.
    # This pipeline starts from savedRecipes (the event collection) rather
    # than recipes, because we want to count save events per recipe.
    # Starting from recipes and doing $size on a joined savedRecipes array
    # would also work, but grouping the event collection with $sum is more
    # direct and performs better at scale.
    most_saved = list(db.savedRecipes.aggregate([

        # Count how many times each recipeId appears in savedRecipes.
        # Each document in savedRecipes is one user saving one recipe,
        # so $sum: 1 per group gives us the bookmark count.
        {"$group": {
            "_id":       "$recipeId",
            "saveCount": {"$sum": 1}
        }},

        # Join back to recipes to get the title — at this point each document
        # is just {_id: recipeId, saveCount: N}, with no recipe data attached
        {"$lookup": {
            "from":         "recipes",
            "localField":   "_id",
            "foreignField": "_id",
            "as":           "recipe"
        }},

        # $lookup always produces an array; flatten it to a single object
        {"$unwind": "$recipe"},

        # Reshape: convert the ObjectId to a string and surface the title
        {"$project": {
            "_id":       {"$toString": "$_id"},
            "title":     "$recipe.title",
            "saveCount": 1
        }},

        {"$sort":  {"saveCount": -1}},
        {"$limit": 5},
    ]))

    return render_template("dashboard.html",
        recipes_per_category=recipes_per_category,
        top_rated=top_rated,
        most_saved=most_saved,
    )
