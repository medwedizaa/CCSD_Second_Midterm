from flask import Flask, render_template
import requests
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection info (Docker will set these as env vars)
DB_HOST = os.environ.get("DB_HOST", "mysql")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_NAME = os.environ.get("DB_NAME", "cats")

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )

@app.route('/')
def home():
    # Get a random cat image
    cat_data = requests.get("https://api.thecatapi.com/v1/images/search").json()
    cat_url = cat_data[0]["url"]

    # Save the cat URL to database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO cat_images (url) VALUES (%s)", (cat_url,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

    # Retrieve recent cats
    cats = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT url FROM cat_images ORDER BY id DESC LIMIT 5")
        cats = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Read error: {e}")

    return render_template("index.html", cat_url=cat_url, cats=cats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

