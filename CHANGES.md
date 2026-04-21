# Update Summary — 2026-04-21

**Author:** Daniel Weidenaar  
**Branch:** daniel/week4-progress

---

## What Was Done

### 1. Blueprint Routes (Backend)

All Flask blueprints are now fully implemented.

| Blueprint | Routes |
|-----------|--------|
| `recipes.py` | GET /recipes (search + filter), GET /recipes/\<id\> (aggregation), POST, PUT, DELETE |
| `users.py` | GET /users, GET /users/\<id\> (with savedRecipes + mealPlans), POST |
| `reviews.py` | GET /reviews/\<recipe_id\>, POST (rating 1–5 validated), DELETE |
| `meal_plans.py` | GET /meal-plans/\<user_id\>, POST, PUT, DELETE |
| `recommendations.py` | GET /recommendations/\<user_id\> — Advanced Feature 1 |
| `dashboard.py` | GET /dashboard — Advanced Feature 2 |

### 2. Advanced Features

**Recommendation Engine** (`GET /recommendations/<user_id>`)  
Matches recipes against user's `dietaryPreferences` and `favoriteCategories` using `$or`. Joins reviews via `$lookup`, computes `avgRating` with `$addFields`, sorts descending, limits to 3 results.

**Dashboard** (`GET /dashboard`)  
Three aggregation pipelines returned in one response:
- Recipes per category (`$group`, `$lookup`, `$sum`)
- Top-rated recipes (`$lookup` reviews, `$addFields $avg`, `$sort`, `$limit 5`)
- Most bookmarked (`$group` savedRecipes, `$lookup` recipes, `$sort`, `$limit 5`)

### 3. Atlas Indexes (`create_indexes.py`)

| Index | Collection | Type |
|-------|-----------|------|
| `recipes_text_search` | recipes | TEXT on title, description, tags |
| `recipes_dietaryFlags` | recipes | ASCENDING on dietaryFlags |
| `reviews_recipeId` | reviews | ASCENDING on recipeId |
| `savedRecipes_userId_recipeId` | savedRecipes | Compound unique |
| `users_email` | users | Unique |

### 4. Frontend Scaffold (for Terysa)

New `views.py` blueprint renders Jinja2 templates — no JavaScript needed.

| Page | URL | Features |
|------|-----|---------|
| Recipe list | `/` | Search by keyword, filter by dietary flag or category |
| Recipe detail | `/recipe/<id>` | Full info, avg rating, reviews, add/delete review, delete recipe |
| Add recipe | `/recipe/new` | Full create form with all fields |
| Dashboard | `/stats` | Live stats from MongoDB aggregation pipelines |

Templates written: `base.html`, `index.html`, `recipe_detail.html`, `recipe_form.html`, `dashboard.html`  
Bootstrap 5 CDN included. Terysa only needs to edit `app/static/style.css`.

### 5. README

`README.md` rewritten with full setup instructions, API endpoint table, advanced feature explanations, MongoDB design highlights, and AI assistance disclosure per spec requirements.

---

## Files Changed

**New files:**
- `app/blueprints/recommendations.py`
- `app/blueprints/dashboard.py`
- `app/blueprints/views.py`
- `app/templates/base.html` (rewritten)
- `app/templates/index.html`
- `app/templates/recipe_detail.html`
- `app/templates/recipe_form.html`
- `app/templates/dashboard.html`
- `app/static/style.css`
- `create_indexes.py`
- `README.md` (rewritten)
- `worklog.txt`

**Modified:**
- `app/__init__.py` — registered all blueprints, added secret_key
- `app/blueprints/recipes.py` — full rewrite
- `app/blueprints/users.py` — full rewrite
- `app/blueprints/reviews.py` — full rewrite
- `app/blueprints/meal_plans.py` — full rewrite
- `seed_db.py` — camelCase field names, correct collection names

---

## What's Left

- [ ] Terysa: CSS styling (`app/static/style.css`)
- [ ] Terysa: Any additional frontend pages (user profile, meal plan view)
- [ ] Terry: Section 6.1 basic queries in DB design doc
- [ ] Sydney: Final DB design doc assembly
- [ ] Team: Milestone demo Week 5 (4/30/2026)
- [ ] Team: Final README team contribution summary section
