# Extending-Photo-Storage-with-Public-Key-Cryptography
---

```markdown
# Photo Storage and Sharing Platform

This project is a secure photo storage and sharing platform that allows users to register, upload photos, add friends, and securely share photos using public-key cryptography. The platform supports multiple devices per user and ensures that photos are encrypted before being stored or shared.

---

## Features

- **User Registration**: Users can register with a username and public key.
- **Add Friends**: Users can add friends by specifying their username and public key.
- **Upload Photos**: Users can upload photos, which are encrypted using AES before being stored on the server.
- **View Photos**: Users can view their own photos and photos shared by friends.
- **Share Photos**: Users can securely share photos with friends by encrypting the AES key with the friend's public key.
- **Multi-Device Support**: Users can invite and revoke devices using public keys.

---

## Requirements

- Python 3.12 or higher
- Flask (`pip install flask`)
- Cryptography library (`pip install cryptography`)
- Requests library (`pip install requests`)
- Pytest (`pip install pytest`)

---

## Project Structure

```
Project_01/
├── client.py                # Client-side logic for interacting with the server
├── log_entry.py             # Log entry class for tracking user actions
├── server.py                # Flask server for handling requests
├── Makefile                 # Makefile for running tests
├── tests/
│   └── test_lab2.py         # Unit tests for the project
└── README.md                # This file
```

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone [repository-url]
   cd Project_01
   ```

2. **Install Dependencies**:
   ```bash
   pip install flask cryptography requests pytest
   ```

3. **Start the Server**:
   ```bash
   python server.py
   ```
   The server will start at `http://127.0.0.1:5000`.

4. **Run the Tests**:
   ```bash
   make grade-lab2
   ```

---

## Usage

### Register a User
```python
from client import Client
alice = Client("Alice")
```

### Add a Friend
```python
bob = Client("Bob")
alice.add_friend("Bob")
```

### Upload a Photo
1. Create a sample photo file:
   ```bash
   echo "Sample photo data" > sample.jpg
   ```
2. Upload the photo:
   ```python
   alice.upload_photo("sample.jpg")
   ```

### View Photos
```python
photos = alice.view_photos()
print(photos)
```

### Share a Photo
```python
alice.share_photo("sample.jpg", "Bob")
```

### View Shared Photos
```python
bob_photos = bob.view_photos()
print(bob_photos)
```

---

## Testing

To run the unit tests:
```bash
make grade-lab2
```

---

## Security Features

- **Public-Key Cryptography**: RSA is used for secure key exchange and signatures.
- **AES Encryption**: Photos are encrypted using AES before being uploaded to the server.
- **Secure Sharing**: Photos are shared securely by encrypting the AES key with the friend's public key.

---

## Future Enhancements

1. **Error Handling**: Improve error handling for invalid inputs, network issues, and server errors.
2. **Logging**: Add logging to track user actions and system events.
3. **UI**: Create a simple command-line or web-based interface for interacting with the system.
4. **Database**: Replace the in-memory storage with a database (e.g., SQLite) for persistent data storage.

---

## Contributors

- [Ramis Ali]

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

---

### **How to Use the `README.md`**
1. Save the content above into a file named `README.md` in your project directory.
2. Update the placeholders (e.g., `[Your Name]`, `[repository-url]`) with your actual information.
3. Commit the `README.md` file to your repository:
   ```bash
   git add README.md
   git commit -m "Add README.md file"
   git push
   ```

---

### **Why a `README.md` is Important**
- **Documentation**: It provides a clear overview of your project for anyone who wants to use or contribute to it.
- **Setup Instructions**: It helps users quickly set up and run your project.
- **Usage Examples**: It demonstrates how to use the key features of your project.
- **Credits and License**: It gives credit to contributors and specifies the license under which the project is distributed.

---

