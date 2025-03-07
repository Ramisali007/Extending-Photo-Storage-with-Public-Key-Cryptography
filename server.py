from flask import Flask, request, jsonify
import os
import base64

app = Flask(__name__)

# In-memory storage
users = {}
photos = {}

@app.route("/register", methods=["POST"])
def register():
    """Register a new user with a public key."""
    data = request.json
    username = data.get("username")
    public_key = data.get("public_key")
    if username in users:
        return jsonify({"message": "User already registered!"}), 400
    users[username] = public_key
    return jsonify({"message": "User registered successfully!"})

@app.route("/add_friend", methods=["POST"])
def add_friend():
    """Add a friend to the user's friend list."""
    data = request.json
    username = data.get("username")
    friend = data.get("friend")
    if username not in users or friend not in users:
        return jsonify({"message": "User not found!"}), 404
    return jsonify({"message": f"{friend} added as a friend!"})

@app.route("/upload/<username>", methods=["POST"])
def upload_photo(username):
    """Upload a photo for the specified user."""
    if username not in users:
        return jsonify({"message": "User not found!"}), 404
    data = request.json
    photo_name = data.get("photo_name")
    photo_data = data.get("photo_data")
    if not photo_name or not photo_data:
        return jsonify({"message": "Photo name or data missing!"}), 400
    photos.setdefault(username, []).append({"name": photo_name, "data": photo_data})
    return jsonify({"message": "Photo uploaded successfully!"})

@app.route("/photos/<username>", methods=["GET"])
def view_photos(username):
    """View all photos for the specified user."""
    if username not in users:
        return jsonify({"message": "User not found!"}), 404
    return jsonify({"photos": photos.get(username, [])})

@app.route("/share", methods=["POST"])
def share_photo():
    """Share a photo with a friend."""
    data = request.json
    username = data.get("username")
    friend = data.get("friend")
    photo_name = data.get("photo_name")
    encrypted_key = data.get("encrypted_key")
    if username not in users or friend not in users:
        return jsonify({"message": "User not found!"}), 404
    if not photo_name or not encrypted_key:
        return jsonify({"message": "Photo name or encrypted key missing!"}), 400
    # Simulate sharing by adding the photo to the friend's list
    photos.setdefault(friend, []).append({"name": photo_name, "data": "shared_photo_data"})
    return jsonify({"message": f"Photo '{photo_name}' shared with {friend}!"})

@app.route("/shutdown", methods=["GET"])
def shutdown():
    """Shutdown the server for testing purposes."""
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down..."

if __name__ == "__main__":
    app.run(debug=True)