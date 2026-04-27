# Recip-Ease — Team Testing Guide

## Setup (do this once)

**1. Clone and install**
```bash
git clone <repo-url>
cd recip-ease
pip install -r requirements.txt
```

**2. Create your `.env` file**
```bash
cp .env.example .env
```
Open `.env` and paste your MongoDB Atlas URI. If you don't have one, ask a teammate — everyone can use the same shared Atlas cluster.

**3. Start the app**
```bash
python run.py
```
Open http://127.0.0.1:5000 in your browser.

---

## What to Test

### Recipe List — `GET /`
- You should see a list of recipes pulled from MongoDB.
- **Search:** Type in the search box and submit — results should filter by title/text.
- **Filter by dietary flag:** Select a flag (vegan, gluten-free, etc.) — only matching recipes should appear.
- **Filter by category:** Select a category from the dropdown — only that category should show.

### Create a Recipe — `GET/POST /recipe/new`
- Click **"Add Recipe"** (or go to `/recipe/new`).
- Fill in title, description, category, author, ingredients (one per line), times, servings, tags, and dietary flags.
- Submit — you should be redirected to the home page with a "Recipe added!" flash message.
- The new recipe should appear in the list.

### Recipe Detail — `GET /recipe/<id>`
- Click any recipe title from the list.
- You should see full recipe info: category, author, ingredients, average rating, and all reviews.

### Add a Review — `POST /recipe/<id>/review`
- On the recipe detail page, fill in the review form (select a user, pick a rating 1–5, add a comment).
- Submit — the page should reload showing your new review and an updated average rating.
- **Edge case:** Try submitting a rating of 0 or 6 — you should get a validation error flash.

### Delete a Review — `POST /review/<id>/delete`
- On the recipe detail page, click **Delete** next to any review.
- The review should disappear and the average rating should update.

### Delete a Recipe — `POST /recipe/<id>/delete`
- On the recipe detail page, click **Delete Recipe**.
- You should be redirected to the home page and the recipe should be gone.

### Dashboard — `GET /dashboard`
- Click **Dashboard** in the nav bar.
- You should see three sections:
  - Recipes per category (sorted by count)
  - Top 5 rated recipes (with avg rating and review count)
  - Top 5 most saved recipes

### Recommendations — `GET /recommendations/<user_id>`
- This is a JSON endpoint. Grab a user `_id` from MongoDB (Atlas UI or compass).
- Visit `/recommendations/<that_id>` in the browser.
- You should get a JSON array of up to 3 recipes matching that user's dietary preferences and favorite categories.
- If the user has no preferences set, all recipes are eligible and the top 3 by rating are returned.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `KeyError: MONGO_URI` or connection error | Check your `.env` file has a valid `MONGO_URI` |
| `500` on recipe detail | The recipe may reference a deleted category/user — check Atlas |
| Empty recipe list | Run the seed script if one exists, or add a recipe manually via the form |
| Flash messages not showing | Make sure you're not skipping the redirect — don't hit the POST URL directly |
