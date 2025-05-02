from flask import request, jsonify
from flask_bcrypt import Bcrypt
from app.models.user import User
from app.models.user import db
from app.utils.aes import encrypt, decrypt
import os

bcrypt = Bcrypt()

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400
    
    salt = os.urandom(16).hex()

    password = password + salt
    password = bcrypt.generate_password_hash(password).decode('utf-8')

    username = encrypt(username)
    salt = encrypt(salt)
    new_user = User(username=username, email=email, password=password, salt=salt)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    userInfo = {"name": decrypt(user.username), "email": user.email}

    salt = decrypt(user.salt)
    password = password + salt

    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful', 'user': userInfo}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
