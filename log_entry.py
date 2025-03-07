import datetime
import json

class LogEntry:
    def __init__(self, action, user, details):
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.action = action
        self.user = user
        self.details = details

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "user": self.user,
            "details": self.details
        }

    def save_log(self, filename="logs.json"):
        try:
            with open(filename, "r") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        logs.append(self.to_dict())
        
        with open(filename, "w") as file:
            json.dump(logs, file, indent=4)

# Example usage
if __name__ == "__main__":
    log = LogEntry("UPLOAD_PHOTO", "Alice", "Uploaded sample.jpg")
    log.save_log()
