import os
from flask_bcrypt import Bcrypt
from app.utils.aes import encrypt, decrypt

bcrypt = Bcrypt()

def hash_credential(password):
    salt = os.urandom(16).hex()
    password = password + salt
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    salt = encrypt(salt)
    
    return password, salt

def check_credential(salt, user_password, password):
    salt = decrypt(salt)
    password = password + salt

    return bcrypt.check_password_hash(user_password, password)