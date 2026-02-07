from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

account = {
    "pin": "1234",
    "balance": 1000
}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["pin"] == account["pin"]:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid PIN"}), 401

@app.route("/balance", methods=["GET"])
def get_balance():
    return jsonify({"balance": account["balance"]})

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    amount = float(data["amount"])
    account["balance"] += amount
    return jsonify({"message": "Deposit successful"})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    amount = float(data["amount"])

    if amount > account["balance"]:
        return jsonify({"message": "Insufficient funds"}), 400

    account["balance"] -= amount
    return jsonify({"message": "Withdrawal successful"})

if __name__ == "__main__":
    app.run(debug=True)