from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required,
    unset_jwt_cookies
)

from werkzeug.security import generate_password_hash, check_password_hash
from app.db.connection import get_db_connection
import re

bp = Blueprint('users', __name__)


def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    if email and len(email) > 128:
        return jsonify({'error': 'Email is too long'}), 400

    password = data.get('password')

    if not email or not validate_email(email):
        return jsonify({'error': 'Invalid email'}), 400
    if not password:
        return jsonify({'error': 'Password required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    password_hash = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
        (email, password_hash)
    )
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if not user or not check_password_hash(user[2], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user[0])
    response = jsonify({
        'message': 'Login successful',
        'access_token': access_token
    })

    set_access_cookies(response, access_token)

    cur.close()
    conn.close()

    return response, 200


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200
