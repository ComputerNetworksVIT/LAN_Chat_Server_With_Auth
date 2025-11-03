import socket
import threading
import json
import os
import hashlib

DATA_DIR = "server_data"
CONFIG_PATH = os.path.join(DATA_DIR, "server_config.json")
USERS_PATH = os.path.join(DATA_DIR, "users.json")

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ---------- SETUP ----------
def setup_server():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        print("⚙️  First-time setup detected.")
        admin_user = input("Enter admin username: ").strip()
        admin_pass = input("Enter admin password: ").strip()
        port = input("Enter port number (default 5555): ").strip() or "5555"

        users = {admin_user: {"password": hash_pw(admin_pass), "role": "admin"}}
        json.dump(users, open(USERS_PATH, "w"), indent=4)
        json.dump({"setupDone": True, "port": int(port)}, open(CONFIG_PATH, "w"), indent=4)
        print(f"✅ Setup complete. Admin '{admin_user}' created on port {port}.")
    else:
        print("✅ Setup already completed.\n")

# ---------- LOGIN ----------
def admin_login():
    users = json.load(open(USERS_PATH))
    while True:
        username = input("Admin username: ").strip()
        password = input("Password: ").strip()
        if username in users and users[username]["password"] == hash_pw(password) and users[username]["role"] == "admin":
            print(f"🔑 Logged in as admin '{username}'.")
            return username
        else:
            print("❌ Invalid credentials. Try again.\n")

# ---------- SERVER CORE ----------
def handle_client(conn, addr):
    conn.send(b"Welcome to the LAN Chat!\n")
    conn.close()

def run_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    server.settimeout(1.0)  # 1 second timeout
    print(f"🚀 Server running on port {port}. Press Ctrl+C to stop.")
    try:
        while True:
            try:
                conn, addr = server.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue  # check again for new connections
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
    finally:
        server.close()
        print("✅ Server closed cleanly.")

# ---------- MAIN ----------
if __name__ == "__main__":
    setup_server()
    config = json.load(open(CONFIG_PATH))
    admin_login()
    run_server(config["port"])
