# Recip-Ease

A recipe management web application built with Python FastAPI and MongoDB Atlas. Users can browse recipes, save favorites, write reviews, and plan weekly meals.

## Team

- Daniel Weidenaar
- Terysa Brewer
- Terry McCulley
- Sydney Roney

## Technology Stack

- **Backend:** Python 3, FastAPI, Uvicorn
- **Database:** MongoDB Atlas (PyMongo driver)
- **Frontend:** HTML, CSS, Jinja2 templates
- **Environment:** python-dotenv

## Project Structure

```
recip-ease/
├── app/
│   ├── __init__.py          # App factory — middleware and router registration
│   ├── db.py                # MongoDB connection helper
│   ├── static/              # CSS
│   ├── templates/           # Jinja2 HTML templates
│   └── blueprints/
│       ├── views.py         # HTML routes: home, recipe CRUD, reviews, stats
│       ├── dashboard.py     # JSON API — summary stats (Advanced Feature)
│       ├── recommendations.py  # JSON API — recipe recommendations (Advanced Feature)
│       ├── recipes.py       # Recipe JSON API — list, create, update, delete
│       ├── users.py         # User routes — list, detail, create
│       ├── reviews.py       # Review API — list, create, delete
│       └── meal_plans.py    # Meal plan routes — list, create, update, delete
├── run.py                   # Entry point (uvicorn)
├── seed_db.py               # One-time script: populate database with sample data
├── create_indexes.py        # One-time script: create Atlas indexes
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repo-url>
cd recip-ease
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in the shared Atlas credentials:

```bash
cp .env.example .env
```

```
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/recip_ease?retryWrites=true&w=majority
```

Do not commit `.env` — it is listed in `.gitignore`.

### 5. Seed the database

```bash
python seed_db.py
```

Inserts sample data into all 6 collections: users, categories, recipes, reviews, savedRecipes, mealPlans.

Expected output:
```
Seeded 7 categories
Seeded 51 users
Seeded 27 recipes
Seeded 30 reviews
Seeded 30 savedRecipes
Seeded 27 mealPlans
Seed complete!
```

### 6. Create Atlas indexes

```bash
python create_indexes.py
```

Creates all required indexes (text search on recipes, dietary flag filter, review lookup, saved recipe uniqueness, user email uniqueness).

### 7. Run the application

```bash
python run.py
```

The app will be available at `http://127.0.0.1:8000`.

## Routes

### HTML (views.py)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home — browse and search recipes |
| GET | `/recipe/new` | New recipe form |
| POST | `/recipe/new` | Submit new recipe |
| GET | `/recipe/{id}` | Recipe detail with category, author, reviews, avg rating |
| POST | `/recipe/{id}/delete` | Delete a recipe |
| POST | `/recipe/{id}/review` | Submit a review (rating 1–5) |
| POST | `/review/{id}/delete` | Delete a review |
| GET | `/stats` | Stats page — recipes per category, top rated, most saved |

### JSON API

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/recipes` | List all recipes. Supports `?q=`, `?flag=`, `?category=` |
| GET | `/recipes/{id}` | Recipe detail with category, author, reviews, avg rating |
| POST | `/recipes` | Create a recipe |
| PUT | `/recipes/{id}` | Update a recipe |
| DELETE | `/recipes/{id}` | Delete a recipe |
| GET | `/users` | List all users |
| GET | `/users/{id}` | User detail with saved recipes and meal plans |
| POST | `/users` | Create a user |
| GET | `/reviews/{recipe_id}` | All reviews for a recipe |
| POST | `/reviews` | Submit a review (rating 1–5 required) |
| DELETE | `/reviews/{id}` | Delete a review |
| GET | `/meal-plans/{user_id}` | All meal plans for a user |
| POST | `/meal-plans` | Create a meal plan |
| PUT | `/meal-plans/{id}` | Update a meal plan |
| DELETE | `/meal-plans/{id}` | Delete a meal plan |
| GET | `/recommendations/{user_id}` | Top 3 recipes matching user's dietary prefs and favorite categories |
| GET | `/dashboard` | Summary stats: recipes per category, top-rated, most saved |

## Advanced Features

### 1. Recommendation Engine (`GET /recommendations/<user_id>`)
Matches recipes against the user's `dietaryPreferences` and `favoriteCategories`. Joins review data, computes average rating, and returns the top 3 highest-rated matches. Uses a multi-stage aggregation pipeline with `$match`, `$lookup`, `$addFields`, `$sort`, and `$limit`.

### 2. Dashboard (`GET /dashboard` and `/stats`)
Returns three summary statistics:
- **Recipes per category** — count of recipes grouped by category name
- **Top-rated recipes** — top 5 by average review rating
- **Most saved recipes** — top 5 by save count

Each statistic uses a separate aggregation pipeline with `$group`, `$lookup`, `$addFields`, and `$sort`.

## MongoDB Design Highlights

- **Embedded documents:** `ingredients` array within recipes; `days` array within meal plans
- **Referenced relationships:** recipes reference `categoryId` and `authorUserId`; reviews reference `userId` and `recipeId`
- **Indexes:** text search index on recipe title/description/tags; compound unique index on savedRecipes; unique index on user email
- **Aggregation:** used in recipe detail, recommendations, and dashboard endpoints

## AI Assistance Disclosure

Claude Code (Anthropic) was used to assist with code generation during development. All team members understand and can explain the database design, collection structure, queries, and application logic.
