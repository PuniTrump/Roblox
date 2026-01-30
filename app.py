from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "votre_cle_secrete_ultra_secure" # Indispensable pour les sessions
CORS(app, supports_credentials=True)

def get_db_connection():
    conn = sqlite3.connect('rouflouxi.db')
    conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par nom
    return conn

# Route de Connexion
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', 
                        (data['email'], data['password'])).fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id'] # On connecte l'utilisateur
        return jsonify({"success": True, "username": user['username']})
    return jsonify({"success": False, "message": "Identifiants incorrects"}), 401

# Route pour récupérer les infos du compte connecté
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Non connecté"}), 401
    
    conn = get_db_connection()
    user = conn.execute('SELECT username, coins, gender FROM users WHERE id = ?', 
                        (session['user_id'],)).fetchone()
    conn.close()
    
    return jsonify({
        "success": True, 
        "username": user['username'], 
        "coins": user['coins'],
        "gender": user['gender']
    })

if __name__ == '__main__':
    app.run(debug=True)
