import pytest
import os
import requests
from client import Client
from log_entry import LogEntry
import json
import subprocess
import time

# Constants
SERVER_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="session", autouse=True)
def setup_server():
    """Start the Flask server in a separate process for testing."""
    # Start the server in a separate process
    server_process = subprocess.Popen(["python", "server.py"])
    # Wait for the server to start
    time.sleep(2)
    yield
    # Teardown: Stop the server after tests
    server_process.terminate()

@pytest.fixture
def alice_client():
    """Create a client for Alice."""
    return Client("Alice")

@pytest.fixture
def bob_client():
    """Create a client for Bob."""
    return Client("Bob")

def test_register(alice_client):
    """Test client registration."""
    assert alice_client.username == "Alice"

def test_add_friend(alice_client, bob_client):
    """Test adding a friend."""
    alice_client.add_friend("Bob")
    # Verify that Bob is added as a friend
    assert True  # Placeholder for actual verification

def test_upload_photo(alice_client):
    """Test uploading a photo."""
    # Create a sample photo file
    with open("sample.jpg", "wb") as file:
        file.write(b"Sample photo data")
    alice_client.upload_photo("sample.jpg")
    # Verify that the photo was uploaded
    assert True  # Placeholder for actual verification

def test_view_photos(alice_client):
    """Test viewing photos."""
    photos = alice_client.view_photos()
    assert photos is not None, "Failed to retrieve photos"
    assert isinstance(photos, dict), "Expected a dictionary of photos"
    assert "photos" in photos, "Photos key not found in response"

def test_share_photo(alice_client, bob_client):
    """Test sharing a photo with a friend."""
    # Upload a photo first
    with open("sample.jpg", "wb") as file:
        file.write(b"Sample photo data")
    alice_client.upload_photo("sample.jpg")
    # Share the photo with Bob
    alice_client.share_photo("sample.jpg", "Bob")
    # Verify that Bob can view the shared photo
    assert True  # Placeholder for actual verification

def test_log_entry():
    """Test log entry creation and saving."""
    log = LogEntry("UPLOAD_PHOTO", "Alice", "Uploaded sample.jpg")
    log.save_log("test_logs.json")
    # Verify that the log entry was saved
    with open("test_logs.json", "r") as file:
        logs = json.load(file)
        assert len(logs) > 0
        assert logs[-1]["user"] == "Alice"