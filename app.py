from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app) # Autorise ton HTML à parler à ton Python

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('rouflouxi.db')
    cursor = conn.cursor()
    # Table des utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            birthday TEXT,
            gender TEXT,
            coins INTEGER DEFAULT 100
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    try:
        conn = sqlite3.connect('rouflouxi.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password, birthday, gender)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['username'], data['email'], data['password'], data['birthday'], data['gender']))
        conn.commit()
        return jsonify({"success": True, "message": "Utilisateur créé !"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Nom d'utilisateur ou email déjà pris"}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
