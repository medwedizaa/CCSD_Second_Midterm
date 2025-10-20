from flask import Flask, render_template
import requests
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Connect to DB
def get_db_connection():
    return mysql.connector.connect(
        host="mysql-server",        # caontainer name from docker-compose.yml
        user="root",
        password="root",
        database="cats_db"
    )

# Table initialization
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_url VARCHAR(255),
            fetched_at DATETIME
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    # Get random cat image from public API
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    image_url = data[0]['url']

    # Save to DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cats (image_url, fetched_at) VALUES (%s, %s)",
        (image_url, datetime.utcnow())
    )
    conn.commit()
    cursor.close()
    conn.close()

    return render_template('index.html', image_url=image_url)

@app.route('/history')
def history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cats ORDER BY fetched_at DESC LIMIT 10")
    cats = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('history.html', cats=cats)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

