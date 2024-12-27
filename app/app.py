from flask import Flask, jsonify, request
import psycopg2
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database connection details
DB_HOST = "db"
DB_NAME = "testdb"
DB_USER = "user"
DB_PASS = "password"

# Establish a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None

# API Routes
@app.route('/')
def home():
    return "Welcome to the 2-Tier Application!"

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users;")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
    user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"id": user_id, "name": name}), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
