# Creates all MongoDB indexes for the Recip-Ease database.
# Run this once after seeding. Re-running is safe because MongoDB skips
# indexes that already exist with the same name and key pattern.
from dotenv import load_dotenv
from pymongo import ASCENDING, TEXT
import os

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from app.db import get_db  # noqa: E402

def create_indexes():
    db = get_db()

    # Full-text search index used by the home page search bar.
    # The $text operator only works on fields covered by a text index.
    # Without this, text searches return nothing and no error is raised.
    db.recipes.create_index(
        [("title", TEXT), ("description", TEXT), ("tags", TEXT)],
        name="recipes_text_search"
    )
    print("Created: recipes_text_search (title, description, tags)")

    # Supports the dietary flag filter on the home page (equality query on dietary_flags).
    db.recipes.create_index(
        [("dietary_flags", ASCENDING)],
        name="recipes_dietaryFlags"
    )
    print("Created: recipes_dietaryFlags")

    # Speeds up fetching all reviews for a recipe, used on the detail page
    # and in the recommendation and dashboard aggregation pipelines.
    db.reviews.create_index(
        [("recipe_id", ASCENDING)],
        name="reviews_recipeId"
    )
    print("Created: reviews_recipeId")

    # Compound unique index on saved_recipes prevents a user from saving
    # the same recipe twice. The uniqueness is enforced at the database level.
    db.saved_recipes.create_index(
        [("user_id", ASCENDING), ("recipe_id", ASCENDING)],
        unique=True,
        name="saved_recipes_userId_recipeId"
    )
    print("Created: saved_recipes_userId_recipeId (unique)")

    # Unique index on email prevents two accounts with the same address.
    db.users.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="users_email"
    )
    print("Created: users_email (unique)")

    print("\nAll indexes created. Verifying...")
    for col in ["recipes", "reviews", "saved_recipes", "users"]:
        indexes = db[col].index_information()
        for name, info in indexes.items():
            if name != "_id_":
                print(f"  {col}.{name}: {info['key']}")

if __name__ == "__main__":
    create_indexes()
