"""Khoroch Tracker - ekta choto offline expense tracker (Flask + SQLite)."""
import os
import sqlite3
from datetime import date

from flask import Flask, redirect, render_template, request, url_for

DATA_DIR = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
DB_PATH = os.path.join(DATA_DIR, "expenses.db")
CATEGORIES = ["Khabar", "Transport", "Bill", "Shopping", "Onnano"]

app = Flask(__name__)


def get_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                category TEXT NOT NULL,
                note TEXT,
                amount REAL NOT NULL
            )"""
        )


@app.route("/")
def index():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM expenses ORDER BY day DESC, id DESC").fetchall()
        total = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
        by_cat = conn.execute(
            "SELECT category, SUM(amount) AS s FROM expenses GROUP BY category ORDER BY s DESC"
        ).fetchall()
    return render_template(
        "index.html", rows=rows, total=total, by_cat=by_cat,
        categories=CATEGORIES, today=date.today().isoformat(),
    )


@app.route("/add", methods=["POST"])
def add():
    try:
        amount = float(request.form["amount"])
    except (KeyError, ValueError):
        return redirect(url_for("index"))
    if amount > 0:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO expenses (day, category, note, amount) VALUES (?, ?, ?, ?)",
                (
                    request.form.get("day") or date.today().isoformat(),
                    request.form.get("category", "Onnano"),
                    request.form.get("note", "").strip(),
                    amount,
                ),
            )
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    # VS Code / local run: python app.py
    app.run(host="127.0.0.1", port=5000, debug=True)
