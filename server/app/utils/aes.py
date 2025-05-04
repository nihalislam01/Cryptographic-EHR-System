import os
from dotenv import load_dotenv
load_dotenv()
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

AES_KEY = os.getenv("AES_KEY")
key = base64.b64decode(AES_KEY)

def encrypt(plain_text):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    padded_data = pad(plain_text.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def encrypt_pdf(pdf_bytes):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    padded_data = pad(pdf_bytes, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext


def decrypt(ciphertext_base64):
    ciphertext_data = base64.b64decode(ciphertext_base64)
    iv = ciphertext_data[:16]
    ciphertext = ciphertext_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv) 
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size).decode('utf-8')
    return plaintext

def decrypt_pdf(encrypted_bytes):
    iv = encrypted_bytes[:AES.block_size]
    ciphertext = encrypted_bytes[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted

def aes_ecb_encrypt(plaintext: str) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plaintext.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode('utf-8')

def aes_ecb_decrypt(ciphertext_b64: str) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = base64.b64decode(ciphertext_b64)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode('utf-8')