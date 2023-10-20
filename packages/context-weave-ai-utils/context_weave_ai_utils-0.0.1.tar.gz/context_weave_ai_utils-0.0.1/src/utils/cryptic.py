import os
from cryptography.fernet import Fernet


# Encryption and decryption functions using Fernet
def encrypt(s:str):
    key = os.getenv("F_KEY")
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(s.encode()).decode()
    return encrypted_text

def decrypt(encrypted_text:str):
    key = os.getenv("F_KEY")
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text
