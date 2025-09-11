from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'msg':'username, email and password required'}), 400

    if User.query.filter((User.username==username) | (User.email==email)).first():
        return jsonify({'msg':'user or email already exists'}), 400

    pw_hash = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=pw_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg':'user created'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg':'username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'msg':'invalid credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token, 'user': {'id': user.id, 'username': user.username}}), 200
