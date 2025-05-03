import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

KEY_DIR = 'keys'
SIG_DIR = 'signatures'
os.makedirs(KEY_DIR, exist_ok=True)
os.makedirs(SIG_DIR, exist_ok=True)

def generate_keypair(doctor_id):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    priv_path = os.path.join(KEY_DIR, f'{doctor_id}_private.pem')
    with open(priv_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    pub_path = os.path.join(KEY_DIR, f'{doctor_id}_public.pem')
    with open(pub_path, 'wb') as f:
        f.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return True

def sign_bytes(doctor_id: str, data: bytes) -> bytes:
    private_key_path = os.path.join(KEY_DIR, f'{doctor_id}_private.pem')
    private_key = RSA.import_key(open(private_key_path).read())
    h = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def verify_signature(doctor_id: str, data: bytes, signature: bytes) -> bool:
    try:
        public_key_path = os.path.join(KEY_DIR, f'{doctor_id}_public.pem')
        public_key = RSA.import_key(open(public_key_path).read())
        h = SHA256.new(data)
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False