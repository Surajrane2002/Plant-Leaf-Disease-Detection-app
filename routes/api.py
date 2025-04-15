from flask import Blueprint, request, jsonify, current_app
from flask_cors import CORS
from config import mysql
import logging

api = Blueprint('api', __name__)
CORS(api)  # Enable Cross-Origin Resource Sharing

# Set up logging
logging.basicConfig(level=logging.INFO)

# ✅ Test API
@api.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"})


# ✅ Signup API
@api.route('/signup', methods=['POST'])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")  # later hash this

    if not all([username, email, password]):
        return jsonify({"message": "All fields are required"}), 400

    conn = None
    cursor = None
    try:
        mysql_instance = current_app.mysql
        conn = mysql_instance.connect()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"message": "User already exists"}), 409

        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()

        return jsonify({"message": "Signup successful"}), 200
    except Exception as e:
        logging.error("Signup Error: %s", str(e))
        return jsonify({"message": "Signup failed", "error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ✅ Login API
@api.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    conn = None
    cursor = None
    try:
        mysql_instance = current_app.mysql
        conn = mysql_instance.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, email, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            stored_hash = user[3]
            if password == stored_hash:  # You can replace this with password hashing
                user_data = {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2]
                }
                return jsonify({"message": "Login successful", "user": user_data}), 200
            else:
                return jsonify({"error": "Invalid password"}), 401
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error("Login Error: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ✅ Store Prediction Results
@api.route('/store_prediction', methods=['POST'])
def store_prediction():
    data = request.json
    logging.info("Received data: %s", data)

    user_id = data.get('user_id')
    image_path = data.get('image_path')
    prediction_result = data.get('prediction_result')
    confidence = data.get('confidence')

    if not all([user_id, image_path, prediction_result, confidence]):
        return jsonify({"error": "Missing required fields"}), 400

    if not (0 <= confidence <= 1):
        return jsonify({"error": "Confidence must be between 0 and 1"}), 400

    conn = None
    cursor = None
    try:
        mysql_instance = current_app.mysql
        conn = mysql_instance.connect()
        cursor = conn.cursor()

        query = "INSERT INTO predictions (user_id, image_path, prediction_result, confidence) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, image_path, prediction_result, confidence))
        conn.commit()

        return jsonify({"message": "Prediction stored successfully"}), 201
    except Exception as e:
        logging.error("Prediction Error: %s", str(e))
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ✅ Get All Predictions
@api.route('/get_predictions', methods=['GET'])
def get_predictions():
    conn = None
    cursor = None
    try:
        mysql_instance = current_app.mysql
        conn = mysql_instance.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM predictions")
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in data]

        return jsonify(results), 200
    except Exception as e:
        logging.error("Get Predictions Error: %s", str(e))
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
