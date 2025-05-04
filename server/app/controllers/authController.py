from flask import request, jsonify
from app.models.user import User, db
from app.utils.aes import encrypt, decrypt, aes_ecb_encrypt, aes_ecb_decrypt
from app.utils.jwtHelper import generate_token
from app.utils.auth import jwt_required
from app.utils.credentialHelper import hash_credential, check_credential
from app.utils.rsa import generate_keypair

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    email = aes_ecb_encrypt(email)
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    password, salt = hash_credential(password)
    username = encrypt(username)
    role = aes_ecb_encrypt('patient')
    new_user = User(username=username, email=email, password=password, salt=salt, role=role)
    db.session.add(new_user)
    db.session.commit()

    generate_keypair(new_user.id)

    return jsonify({'message': 'User registered successfully'}), 201

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    email = aes_ecb_encrypt(email)
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user and check_credential(user.salt, user.password, password):
        token = generate_token(user.id)
        userInfo = {"name": decrypt(user.username), "email": aes_ecb_decrypt(user.email), "role": aes_ecb_decrypt(user.role)}
        return jsonify({'message': 'Login successful', 'user': userInfo, 'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@jwt_required
def check_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_info = {
        "name": decrypt(user.username),
        "email": aes_ecb_decrypt(user.email),
        "role": aes_ecb_decrypt(user.role),
    }
    return jsonify({'user': user_info}), 200
