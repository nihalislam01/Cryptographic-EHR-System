from flask import request, jsonify
from app.models.user import User, db
from app.utils.aes import encrypt, decrypt
from app.utils.jwtHelper import generate_token
from app.utils.auth import jwt_required
from app.utils.credentialHelper import hash_credential, check_credential
from app.utils.rsa import generate_keypair

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    password, salt = hash_credential(password)
    username = encrypt(username)
    new_user = User(username=username, email=email, password=password, salt=salt)
    db.session.add(new_user)
    db.session.commit()

    generate_keypair(new_user.id)

    return jsonify({'message': 'User registered successfully'}), 201

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    userInfo = {"name": decrypt(user.username), "email": user.email, "role": user.role}

    if user and check_credential(user.salt, user.password, password):
        token = generate_token(user.id)
        return jsonify({'message': 'Login successful', 'user': userInfo, 'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@jwt_required
def check_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_info = {
        "name": decrypt(user.username),
        "email": user.email,
        "role": user.role,
    }
    return jsonify({'user': user_info}), 200
