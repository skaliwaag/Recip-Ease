from dotenv import load_dotenv
from pymongo import ASCENDING, TEXT
import os

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from app.db import get_db

def create_indexes():
    db = get_db()

    # recipes — full-text keyword search across title, description, tags
    db.recipes.create_index(
        [("title", TEXT), ("description", TEXT), ("tags", TEXT)],
        name="recipes_text_search"
    )
    print("Created: recipes_text_search (title, description, tags)")

    # recipes — dietary flag filter
    db.recipes.create_index(
        [("dietaryFlags", ASCENDING)],
        name="recipes_dietaryFlags"
    )
    print("Created: recipes_dietaryFlags")

    # reviews — fetch all reviews for a recipe
    db.reviews.create_index(
        [("recipeId", ASCENDING)],
        name="reviews_recipeId"
    )
    print("Created: reviews_recipeId")

    # savedRecipes — bookmark lookups and duplicate prevention
    db.savedRecipes.create_index(
        [("userId", ASCENDING), ("recipeId", ASCENDING)],
        unique=True,
        name="savedRecipes_userId_recipeId"
    )
    print("Created: savedRecipes_userId_recipeId (unique)")

    # users — prevent duplicate accounts
    db.users.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="users_email"
    )
    print("Created: users_email (unique)")

    print("\nAll indexes created. Verifying...")
    for col in ["recipes", "reviews", "savedRecipes", "users"]:
        indexes = db[col].index_information()
        for name, info in indexes.items():
            if name != "_id_":
                print(f"  {col}.{name}: {info['key']}")

if __name__ == "__main__":
    create_indexes()
