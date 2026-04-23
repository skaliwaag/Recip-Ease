from flask import Blueprint
import sqlite3

# Database setup for meal plans
meal_plans_bp = Blueprint("meal_plans", __name__)

# Database connection and CRUD operations for meal plans
def get_db():
    conn = sqlite3.connect('mealplans.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE meal plan
def create_mealplan(user_id, week_start, days, notes):
    db = get_db()
    db.execute('INSERT INTO mealplan (userid, weekstart, days, notes) VALUES (?, ?, ?, ?)',
               (user_id, week_start, days, notes))
    db.commit()

# READ meal plan
def read_mealplan(mealplan_id: int):
    db = get_db()
    return db.execute('SELECT * FROM mealplan WHERE id = ?', (mealplan_id,)).fetchone()

# UPDATE meal plan
def update_mealplan(mealplan):
    db = get_db()
    db.execute('UPDATE mealplan SET userid = ?, weekstart = ?, days = ?, notes = ? WHERE id = ?',
               (mealplan.userid, mealplan.weekstart, mealplan.days, mealplan.notes, mealplan.id))
    db.commit()

# DELETE meal plan
def delete_mealplan(mealplan_id: int):
    db = get_db()
    db.execute('DELETE FROM mealplan WHERE id = ?', (mealplan_id,))
    db.commit()
