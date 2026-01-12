from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from argon2 import PasswordHasher
import base64
import os

class CryptoEngine:
    def __init__(self):
        self.ph = PasswordHasher()
        self._key = None
    
    def hash_password(self, password: str) -> tuple[str, str]:
        """Hash password using Argon2, returns (hash, salt)"""
        salt = base64.b64encode(get_random_bytes(16)).decode('utf-8')
        password_hash = self.ph.hash(password + salt)
        return password_hash, salt
    
    def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        try:
            self.ph.verify(password_hash, password + salt)
            return True
        except:
            return False
    
    def derive_key(self, password: str, salt: str) -> bytes:
        """Derive encryption key from password"""
        salt_bytes = base64.b64decode(salt.encode('utf-8'))
        self._key = PBKDF2(password, salt_bytes, dkLen=32, count=100000)
        return self._key
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using AES-GCM"""
        if not self._key:
            raise ValueError("Key not derived. Call derive_key first.")
        nonce = get_random_bytes(12)
        cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
        encrypted = base64.b64encode(nonce + tag + ciphertext).decode('utf-8')
        return encrypted
    
    def decrypt(self, encrypted: str) -> str:
        """Decrypt ciphertext using AES-GCM"""
        if not self._key:
            raise ValueError("Key not derived. Call derive_key first.")
        data = base64.b64decode(encrypted.encode('utf-8'))
        nonce, tag, ciphertext = data[:12], data[12:28], data[28:]
        cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')
    
    def clear_key(self):
        """Zero out the key from memory"""
        if self._key:
            self._key = b'\x00' * len(self._key)
            self._key = None
