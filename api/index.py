import os
import psycopg2
from flask import Flask, request, jsonify
from . import scripts
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        #port=os.environ.get("DB_PORT", 5432),
        dbname=os.environ["POSTGRES_DATABASE"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"]
        #sslmode=os.environ.get("DB_SSLMODE", "require")  # optional, but recommended for hosted DBs
    )
    return conn

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    print(data)
    print(data.keys())

    # Basic validation
    username = data.get("username")
    no_of_games = data.get("no_of_games")
    print(username)
    print(no_of_games)

    if not username:
        return jsonify({"error": "username and no_of_games are required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            scripts.CREATE_USER,
            (username, no_of_games)
        )
        new_user = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "id": new_user[0],
            "username": new_user[1],
            "no_of_games": new_user[2]
        }), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500