# Recip-Ease

A recipe management web application built with Python Flask and MongoDB Atlas. Users can browse recipes, save favorites, write reviews, and plan weekly meals.

## Team

- Daniel Weidenaar
- Terysa Brewer
- Terry McCulley
- Sydney Roney

## Technology Stack

- **Backend:** Python 3, Flask
- **Database:** MongoDB Atlas (PyMongo driver)
- **Frontend:** HTML, CSS, Jinja2 templates
- **Environment:** python-dotenv

## Project Structure

```
recip-ease/
├── app/
│   ├── __init__.py          # App factory, blueprint registration
│   ├── db.py                # MongoDB connection helper
│   └── blueprints/
│       ├── recipes.py       # CRUD + search/filter
│       ├── users.py         # User management
│       ├── reviews.py       # Recipe reviews
│       ├── meal_plans.py    # Weekly meal planning
│       ├── recommendations.py  # Advanced Feature 1
│       └── dashboard.py     # Advanced Feature 2
├── run.py                   # App entry point
├── seed_db.py               # Database seeding script
├── create_indexes.py        # Atlas index creation script
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

Create a `.env` file in the project root:

```
MONGO_URI=mongodb+srv://<username>:<password>@recipe-ease.ajuvsog.mongodb.net/?appName=Recipe-Ease
```

Replace `<username>` and `<password>` with the shared Atlas credentials. Do not commit this file — it is listed in `.gitignore`.

### 5. Seed the database

```bash
python seed_db.py
```

This inserts sample data into all 6 collections: users, categories, recipes, reviews, savedRecipes, mealPlans.

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

This creates all required indexes (text search, dietary flag filter, review lookup, saved recipe uniqueness, user email uniqueness).

### 7. Run the application

```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Recipes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/recipes` | List all recipes. Supports `?q=`, `?flag=`, `?category=` |
| GET | `/recipes/<id>` | Recipe detail with category, author, reviews, avg rating |
| POST | `/recipes` | Create a recipe |
| PUT | `/recipes/<id>` | Update a recipe |
| DELETE | `/recipes/<id>` | Delete a recipe |

### Users
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/users` | List all users |
| GET | `/users/<id>` | User detail with saved recipes and meal plans |
| POST | `/users` | Create a user |

### Reviews
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/reviews/<recipe_id>` | All reviews for a recipe |
| POST | `/reviews` | Submit a review (rating 1–5 required) |
| DELETE | `/reviews/<id>` | Delete a review |

### Meal Plans
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/meal-plans/<user_id>` | All meal plans for a user |
| POST | `/meal-plans` | Create a meal plan |
| PUT | `/meal-plans/<id>` | Update a meal plan |
| DELETE | `/meal-plans/<id>` | Delete a meal plan |

### Advanced Features
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/recommendations/<user_id>` | Top 3 recipe recommendations based on user preferences |
| GET | `/dashboard` | Summary stats: recipes per category, top-rated, most saved |

## Advanced Features

### 1. Recommendation Engine (`GET /recommendations/<user_id>`)
Matches recipes against the user's `dietaryPreferences` and `favoriteCategories`. Joins review data, computes average rating, and returns the top 3 highest-rated matching recipes. Uses a multi-stage aggregation pipeline with `$match`, `$lookup`, `$addFields`, `$sort`, and `$limit`.

### 2. Dashboard (`GET /dashboard`)
Returns three summary statistics in a single response:
- **Recipes per category** — count of recipes grouped by category name
- **Top-rated recipes** — top 5 recipes by average review rating
- **Most bookmarked recipes** — top 5 recipes by number of saves

Each statistic is computed with a separate aggregation pipeline using `$group`, `$lookup`, `$addFields`, and `$sort`.

## MongoDB Design Highlights

- **Embedded documents:** `ingredients` array within recipes; `days` array within meal plans
- **Referenced relationships:** recipes reference `categoryId` and `authorUserId`; reviews reference `userId` and `recipeId`
- **Indexes:** text search index on recipe title/description/tags; compound unique index on savedRecipes; unique index on user email
- **Aggregation:** used in recipe detail, recommendations, and dashboard endpoints

## AI Assistance Disclosure

AI coding tools were used to assist with code generation during development. All team members understand and can explain the database design, collection structure, queries, and application logic.
