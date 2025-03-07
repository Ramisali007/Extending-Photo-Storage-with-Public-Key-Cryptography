import os
import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # Add this import
import base64
import secrets

# Server URL
SERVER_URL = "http://127.0.0.1:5000"

class Client:
    def __init__(self, username):
        self.username = username
        self.private_key, self.public_key = self.generate_keys()
        self.aes_key = self.generate_aes_key()
        self.register()

    def generate_keys(self):
        """Generate RSA key pair (private and public keys)."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def generate_aes_key(self):
        """Generate a secure AES key for encryption."""
        return secrets.token_bytes(32)

    def encrypt_aes(self, plaintext):
        """Encrypt data using AES encryption."""
        iv = secrets.token_bytes(16)  # Random IV
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad plaintext to be a multiple of 16 bytes
        padded_plaintext = plaintext + b" " * (16 - len(plaintext) % 16)
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode()

    def register(self):
        """Register the client with the server using its public key."""
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        response = requests.post(f"{SERVER_URL}/register", json={
            "username": self.username,
            "public_key": public_pem
        })
        print(response.json())

    def add_friend(self, friend_username):
        """Send a friend request to another user."""
        response = requests.post(f"{SERVER_URL}/add_friend", json={
            "username": self.username,
            "friend": friend_username
        })
        print(response.json())

    def upload_photo(self, photo_path):
        """Encrypt and upload a photo to the server."""
        if not os.path.exists(photo_path):
            print("File not found!")
            return

        with open(photo_path, "rb") as file:
            encrypted_photo = self.encrypt_aes(file.read())

        response = requests.post(f"{SERVER_URL}/upload/{self.username}", json={
            "photo_name": os.path.basename(photo_path),
            "photo_data": encrypted_photo
        })
        print(response.json())

    def view_photos(self):
        """View list of photos available on the server."""
        response = requests.get(f"{SERVER_URL}/photos/{self.username}")
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def share_photo(self, photo_name, friend_username):
        """Share a photo securely with a friend."""
        friend_public_key_path = os.path.join("clients", friend_username, "public_key.pem")

        # Check if the friend's public key exists
        if not os.path.exists(friend_public_key_path):
            print(f"Error: Public key for {friend_username} not found.")
            return

        # Read the friend's public key
        with open(friend_public_key_path, "rb") as key_file:
            friend_public_key = serialization.load_pem_public_key(
                key_file.read(), backend=default_backend()
            )

        # Encrypt the AES key using the friend's public key
        encrypted_aes_key = friend_public_key.encrypt(
            self.aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Send the encrypted key to the server
        response = requests.post(f"{SERVER_URL}/share", json={
            "username": self.username,
            "friend": friend_username,
            "photo_name": photo_name,
            "encrypted_key": base64.b64encode(encrypted_aes_key).decode()
        })
        print(response.json())

if __name__ == "__main__":
    alice = Client("Alice")
    bob = Client("Bob")

    # Alice adds Bob as a friend
    alice.add_friend("Bob")

    # Alice uploads a photo
    alice.upload_photo("sample.jpg")

    # Alice shares the photo with Bob
    alice.share_photo("sample.jpg", "Bob")

    # Bob views the available photos
    bob.view_photos()