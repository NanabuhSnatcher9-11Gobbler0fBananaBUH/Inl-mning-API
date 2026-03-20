from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'inlamning_1'
}

@app.route('/', methods=['GET'])
def index():
    return """Hej och välkommen till min API! /users för att se alla användare, /users/id för att se en specifik användare. { "username" : "glugs", "email" : "banana@banan.com",	"name" : "glugfs", 	"password" : "patatr" }"""

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
@app.route('/users', methods=['GET']) 
def get_users():
    """Get all users"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    users = cursor.fetchall()
    if not users: # saknades personen i databasen?
        return jsonify({'error': 'User not found'}), 404

    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET']) #Denna gör så att man kan specifiera id på en användare.
def get_user(user_id):
    """Get all users"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # hämta ENDAST user med id
    sql = "SELECT * FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()
    if not user: # saknades personen i databasen?
        return jsonify({'error': 'User not found'}), 404
       
    return jsonify(user)

@app.route('/users', methods=['POST'])
def user_specifications():
    """User specifications"""
    data = request.get_json()  # Hämta data från requesten.
    username = data.get('username')
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
        
    connection = get_db_connection()
        
    cursor = connection.cursor()
    sql = "INSERT INTO users (username, email, name, password) VALUES (%s, %s,%s, %s)"
    cursor.execute(sql, (username, email, name, password))
        
    connection.commit() # commit() gör klart skrivningen till databasen
    user_id = cursor.lastrowid # cursor.lastrowid innehåller id på raden som skapades i DB
        
    user = {
            'id': user_id,
            'username': username,
            'email': email,
            'name': name,
            'password': password
    } 


    return jsonify(user), 201 # HTTP Status 201 Created

# @app.route('/create', methods=['POST'])
# def create_user():
#     """Create a new user"""
#     data = request.get_json()  # Hämta data från requesten.

#     if is_valid_user_data(data):
#         return jsonify ({"message": "User is created"}), 201
#     else:
#         return jsonify({"error": "Missing field"}), 400

def is_valid_user_data(data):
    return data and 'username' in data and 'email' in data and 'name' in data and 'password' in data


if __name__ == '__main__':
    app.run(debug=True, port=5000)
