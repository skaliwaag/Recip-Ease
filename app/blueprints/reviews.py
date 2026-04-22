from flask import Blueprint
import sqlite3

reviews_bp = Blueprint("reviews", __name__)

def get_db():
    conn = sqlite3.connect('mealplans.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_review(user_id, recipe_id, rating, comment, created_at):
    db = get_db()
    db.execute('INSERT INTO users (user_id, recipe_id, rating, comment, created at) VALUES (?, ?, ?, ?)',
               (user_id, recipe_id, rating, comment, created_at))
    db.commit()
    

def read_review(user_id: int):
    db = get_db()
    return db.execute('SELECT * FROM reviews WHERE user_id = ?', (user_id,)).fetchone()

    
def update_reviews(reviews):
    db = get_db()
    db.execute('UPDATE reviews SET recipe_id = ?, rating = ?, comment = ? WHERE user_id = ?',
               (reviews.user_id, reviews.recipe_id, reviews.rating, reviews.comment, reviews.created_at))
    db.commit()

def delete_user(user_id: int):
    db = get_db()
    db.execute('DELETE FROM reviews WHERE user_id = ?', (user_id,))
    db.commit()
