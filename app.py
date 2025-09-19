from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "budget.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        category TEXT,
        amount REAL
    )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = cur.fetchall()
    cur.execute("SELECT SUM(amount) FROM transactions")
    balance = cur.fetchone()[0] or 0.0
    conn.close()
    return render_template("index.html", transactions=transactions, balance=balance)

@app.route("/add", methods=["POST"])
def add_transaction():
    description = request.form["description"]
    category = request.form["category"]
    amount = float(request.form["amount"])
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (date, description, category, amount) VALUES (?, ?, ?, ?)",
                (datetime.now().strftime("%Y-%m-%d"), description, category, amount))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
