from flask import Blueprint
import sqlite3

meal_plans_bp = Blueprint("meal_plans", __name__)


def get_db():
    conn = sqlite3.connect('mealplans.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_mealplan(user_id, week_start, days, notes):
    db = get_db()
    db.execute('INSERT INTO mealplan (userid, weekstart, days, notes) VALUES (?, ?, ?, ?)',
               (user_id, week_start, days, notes))
    db.commit()

def read_mealplan(mealplan_id: int):
    db = get_db()
    return db.execute('SELECT * FROM mealplan WHERE id = ?', (mealplan_id,)).fetchone()

def update_mealplan(mealplan):
    db = get_db()
    db.execute('UPDATE mealplan SET userid = ?, weekstart = ?, days = ?, notes = ? WHERE id = ?',
               (mealplan.userid, mealplan.weekstart, mealplan.days, mealplan.notes, mealplan.id))
    db.commit()

def delete_mealplan(mealplan_id: int):
    db = get_db()
    db.execute('DELETE FROM mealplan WHERE id = ?', (mealplan_id,))
    db.commit()
