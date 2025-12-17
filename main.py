import flask
import sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
    storage_uri="memory://",
)

conn = sqlite3.connect('gifts.db') 
cursor = conn.cursor()  
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gift TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
''')
conn.commit()  
conn.close()

@app.get("/")
@limiter.exempt
def index():
    return flask.send_from_directory("static", "index.html")

@app.post("/gifts")
def create_gift():
    data = flask.request.get_json()
    name = data.get('name')
    gift = data.get('gift')
    
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gifts (name, gift) VALUES (?, ?)', (name, gift))
    conn.commit()
    conn.close()

    return '', 201
    
@app.get("/gifts")
def get_gifts():
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, gift, completed FROM gifts')
    rows = cursor.fetchall()
    conn.close()
    
    gifts = [{'id': row[0], 'name': row[1], 'gift': row[2], 'completed': bool(row[3])} for row in rows]
    return flask.jsonify(gifts)

@app.patch("/gifts/<int:gift_id>")
def update_gift(gift_id):
    data = flask.request.get_json()
    completed = data.get('completed', False)
    
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE gifts SET completed = ? WHERE id = ?', (int(completed), gift_id))
    conn.commit()
    conn.close()
    
    return '', 204

if __name__ == "__main__":
    app.run()