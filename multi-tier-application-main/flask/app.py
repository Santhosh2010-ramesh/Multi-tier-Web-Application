from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# Load MySQL credentials from environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql.default.svc.cluster.local")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "mydb")

def get_db_connection():
    """Establish a connection to MySQL with retry mechanism"""
    for _ in range(5):  # Retry up to 5 times
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            print("✅ Connected to MySQL successfully!")
            return conn
        except mysql.connector.Error as err:
            print(f"❌ MySQL Connection Error: {err}")
            time.sleep(2)
    return None

@app.route("/")
def hello():
    return "Hello from Flask with MySQL!"

@app.route("/users")
def get_users():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Debug: Check selected database
        cursor.execute("SELECT DATABASE();")
        db_selected = cursor.fetchone()
        print(f"Connected to database: {db_selected}")
        
        # Ensure table name is correctly referenced
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(f"Available tables: {tables}")
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return jsonify(users)
    except mysql.connector.Error as err:
        return jsonify({"error": f"MySQL Error: {err}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
