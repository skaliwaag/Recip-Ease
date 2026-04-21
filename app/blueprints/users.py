from flask import Blueprint
import sqlite3


users_bp = Blueprint("users", __name__)


def get_db():
    conn = sqlite3.connect('mealplans.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_user(name, email, dietary_preferences, favorite_categories, created_at):
    db = get_db()
    db.execute('INSERT INTO users (name, email, dietary_preferences, favorite_catergories, created at) VALUES (?, ?, ?, ?)',
               (name, email, dietary_preferences, favorite_categories, created_at))
    db.commit()
    

def read_user(name: str):
    db = get_db()
    return db.execute('SELECT * FROM users WHERE name = ?', (name)).fetchone()

    
def update_user(users):
    db = get_db()
    db.execute('UPDATE users SET email = ?, dietary_preferences = ?, favorite_categories = ? WHERE name = ?',
               (users.name, users.email, users.dietary_preferences, users.favorite_categories, users.created_at))
    db.commit()

def delete_user(name: str):
    db = get_db()
    db.execute('DELETE FROM user WHERE name = ?', (name,))
    db.commit()
