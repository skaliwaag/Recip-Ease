from app.db import get_db
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def seed():
    db = get_db()

    # ── CLEAR ──
    db.users.drop()
    db.categories.drop()
    db.recipes.drop()
    db.reviews.drop()
    db.saved_recipes.drop()
    db.meal_plans.drop()
    print("Cleared collections.")

    # ── CATEGORIES ──
    categories = db.categories.insert_many([
        { "name": "Dinner", "description": "Evening meals", "tags": ["hearty", "main course"] },
    ]).inserted_ids

    # ── USERS ──
    users = db.users.insert_many([
        {
            "name": "Maria Santos",
            "email": "maria@example.com",
            "dietary_preferences": ["vegetarian", "gluten-free"],
            "favorite_categories": [categories[0]],
        },
    ]).inserted_ids

    # ── RECIPES ──
    recipes = db.recipes.insert_many([
        {
            "title": "Chicken Tikka Masala",
            "description": "A rich, creamy tomato-based curry.",
            "category_id": categories[0],
            "author_user_id": users[0],
            "ingredients": [
                { "name": "chicken breast", "amount": 500, "unit": "g" },
                { "name": "heavy cream",    "amount": 200, "unit": "ml" },
                { "name": "garam masala",   "amount": 2,   "unit": "tsp" },
            ],
            "tags": ["curry", "Indian", "comfort food"],
            "dietary_flags": ["gluten-free", "high-protein"],
            "prep_time": 20,
            "cook_time": 35,
            "servings": 4,
        },
    ]).inserted_ids

    # ── REVIEWS ──
    reviews = db.reviews.insert_many([
        {
            "user_id":   users[0],
            "recipe_id": recipes[0],
            "rating":    5,
            "comment":   "Perfect level of spice.",
        },
    ]).inserted_ids

    # ── SAVED RECIPES ──
    saved = db.saved_recipes.insert_many([
        { "user_id": users[0], "recipe_id": recipes[0] },
    ]).inserted_ids

    # ── MEAL PLANS ──
    meal_plans = db.meal_plans.insert_many([
        {
            "user_id": users[0],
            "week_start": datetime(2026, 4, 13),
            "days": [
                { "day": "Monday", "recipe_id": recipes[0], "notes": "" },
            ],
            "notes": "Test week.",
        },
    ]).inserted_ids

    print("✓ Seed complete — 1 document per collection.")

if __name__ == "__main__":
    seed()