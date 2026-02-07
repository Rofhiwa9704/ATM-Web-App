import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Create or connect to database
def get_db_connection():
    conn = sqlite3.connect("atm.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table and default user
def setup_database():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY,
            pin TEXT,
            balance REAL
        )
    """)
    conn.commit()

    check = conn.execute("SELECT * FROM account").fetchone()
    if check is None:
        conn.execute(
            "INSERT INTO account (pin, balance) VALUES (?, ?)",
            ("1234", 1000)
        )
        conn.commit()
    conn.close()

setup_database()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM account WHERE pin = ?",
        (data["pin"],)
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid PIN"}), 401

@app.route("/balance", methods=["GET"])
def balance():
    conn = get_db_connection()
    bal = conn.execute(
        "SELECT balance FROM account WHERE id = 1"
    ).fetchone()["balance"]
    conn.close()
    return jsonify({"balance": bal})

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    amount = float(data["amount"])

    conn = get_db_connection()
    conn.execute(
        "UPDATE account SET balance = balance + ? WHERE id = 1",
        (amount,)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Deposit successful"})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    amount = float(data["amount"])

    conn = get_db_connection()
    balance = conn.execute(
        "SELECT balance FROM account WHERE id = 1"
    ).fetchone()["balance"]

    if amount > balance:
        conn.close()
        return jsonify({"message": "Insufficient funds"}), 400

    conn.execute(
        "UPDATE account SET balance = balance - ? WHERE id = 1",
        (amount,)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Withdrawal successful"})

if __name__ == "__main__":
    app.run(debug=True)