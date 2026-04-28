# Recip-Ease

A recipe management web application built with Python (Flask) and MongoDB Atlas. Users can browse recipes, save favorites, write reviews, plan weekly meals, and receive personalized recipe recommendations.

## Team

- Daniel Weidenaar
- Terysa Brewer
- Terry McCulley
- Sydney Roney

## Technology Stack

- **Backend:** Python 3, Flask 3.1+
- **Database:** MongoDB Atlas (PyMongo 4.8+ driver)
- **Frontend:** Jinja2 server-side templates, Bootstrap 5.3
- **Environment:** python-dotenv

## Project Structure

```
recip-ease/
├── app/
│   ├── __init__.py              # App factory — blueprint registration
│   ├── db.py                    # MongoDB connection helper
│   ├── static/
│   │   └── style.css            # Custom Bootstrap overrides
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html           # Recipe list with search/filter
│   │   ├── recipe_detail.html
│   │   ├── recipe_form.html
│   │   └── dashboard.html
│   └── blueprints/
│       ├── views.py             # HTML routes: home, recipe CRUD, reviews, dashboard
│       ├── recipes.py           # Recipe JSON API
│       ├── users.py             # User JSON API
│       ├── reviews.py           # Review JSON API
│       ├── meal_plans.py        # Meal plan JSON API
│       ├── recommendations.py   # Recommendation engine (Advanced Feature 1)
│       └── dashboard.py         # Summary stats (Advanced Feature 2)
├── run.py                       # Flask dev server entry point
├── seed_db.py                   # One-time script: populate all 6 collections
├── create_indexes.py            # One-time script: create Atlas indexes
├── requirements.txt
├── .env.example                 # Environment variable template
└── TESTING.md                   # Manual testing guide
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repo-url>
cd recip-ease
```

### 2. Run the setup script

```powershell
.\start.bat
```

On first run this will:
- Create a virtual environment and install dependencies
- Open `.env` in Notepad — paste in the shared Atlas `MONGO_URI`, save, and close
- Seed all 6 collections and create Atlas indexes
- Launch the app at `http://127.0.0.1:5000`

On subsequent runs it skips straight to seed → indexes → launch.

Do not commit `.env` — it is listed in `.gitignore`.

## Routes

### HTML (Browser UI)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home — browse and search recipes |
| GET | `/recipe/new` | New recipe form |
| POST | `/recipe/new` | Submit new recipe |
| GET | `/recipe/<id>` | Recipe detail: ingredients, author, reviews, avg rating |
| POST | `/recipe/<id>/delete` | Delete a recipe |
| POST | `/recipe/<id>/review` | Submit a review (rating 1–5) |
| POST | `/review/<id>/delete` | Delete a review |
| GET | `/dashboard` | Dashboard: recipes per category, top-rated, most saved |

### JSON API

#### Recipes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/recipes` | List all recipes. Query params: `?q=`, `?flag=`, `?category=` |
| GET | `/recipes/<id>` | Recipe detail with category, author, avg rating |
| POST | `/recipes` | Create a recipe |
| PUT | `/recipes/<id>` | Update a recipe |
| DELETE | `/recipes/<id>` | Delete a recipe |

#### Users

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/users` | List all users |
| GET | `/users/<id>` | User detail |
| POST | `/users` | Create a user |
| PUT | `/users/<id>` | Update a user |
| DELETE | `/users/<id>` | Delete a user |

#### Reviews

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/reviews` | List all reviews (sorted by date, newest first) |
| GET | `/reviews/<recipe_id>` | All reviews for a specific recipe |
| POST | `/reviews` | Submit a review (rating 1–5 required) |
| PUT | `/reviews/<id>` | Update a review (rating and/or comment) |
| DELETE | `/reviews/<id>` | Delete a review |

#### Meal Plans

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/meal-plans/<user_id>` | All meal plans for a user (sorted by week, newest first) |
| POST | `/meal-plans` | Create a meal plan |
| PUT | `/meal-plans/<id>` | Update a meal plan |
| DELETE | `/meal-plans/<id>` | Delete a meal plan |

#### Advanced Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/recommendations/<user_id>` | Top 3 recipes matching user's dietary preferences and favorite categories |
| GET | `/dashboard` | Summary stats: recipes per category, top-rated (5), most saved (5) |

## Advanced Features

### 1. Recommendation Engine (`GET /recommendations/<user_id>`)

Fetches the user's `dietary_preferences` and `favorite_categories`, then runs a multi-stage aggregation pipeline to find recipes that match both. Joins review data via `$lookup`, computes average rating with `$addFields`, sorts by rating descending, and returns the top 3 results. Stages used: `$match`, `$lookup`, `$addFields`, `$sort`, `$limit`.

### 2. Dashboard (`GET /dashboard`)

Returns three aggregated statistics, each from its own pipeline:

- **Recipes per category** — `$group` by category, `$lookup` to resolve category name, sorted by count
- **Top-rated recipes** — `$lookup` reviews, `$addFields` avg rating, top 5 by rating
- **Most saved recipes** — `$group` by recipe, `$lookup` recipe title, top 5 by save count

## Database Design

### Collections

| Collection | Documents | Purpose |
|------------|-----------|---------|
| `users` | 51 | Accounts with dietary preferences and favorite categories |
| `categories` | 7 | Breakfast, Lunch, Dinner, Dessert, Snack, Appetizer, Comfort |
| `recipes` | 27 | Full recipe data with embedded ingredients array |
| `reviews` | 30 | Ratings (1–5) and comments, referenced to recipe and user |
| `saved_recipes` | 30 | User–recipe bookmarks (join collection) |
| `meal_plans` | 27 | Weekly plans with embedded days array per user |

### Design Highlights

- **Embedded documents:** `ingredients` array inside each recipe; `days` array inside each meal plan
- **Referenced relationships:** recipes reference `category_id` and `author_user_id`; reviews reference `user_id` and `recipe_id`
- **Indexes:** text search on recipe title/description/tags; dietary flag filter index; compound unique index on saved recipes; unique index on user email
- **Aggregation pipelines:** used in recipe detail, recommendations, and all dashboard statistics

## AI Assistance Disclosure

A Claude/Anthropic AI agent was used for project planning, codebase scaffolding, rubric compliance checks, and troubleshooting, as well as document formatting assistance. All team members understand and can explain the database design, collection structure, queries, and application logic.
