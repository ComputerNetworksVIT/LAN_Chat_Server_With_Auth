import socket
import threading

# ---------- CONFIG ----------
def get_local_ip():
    """Find local IP (useful for LAN testing)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

HOST = "0.0.0.0"
PORT = 5555
clients = {}

# ---------- PROTOCOL HELPERS ----------
def decode_lantp(packet):
    """Parse raw LANTP message into a dict."""
    lines = packet.strip().split("\n")
    if not lines or not lines[0].startswith("LANTP/1.0"):
        return None
    data = {}
    for line in lines[1:]:
        if line.strip() == "<END>":
            break
        if ": " in line:
            key, val = line.split(": ", 1)
            data[key] = val
    return data

def encode_lantp(data):
    """Convert a dict into LANTP/1.0 formatted message."""
    lines = ["LANTP/1.0"]
    for k, v in data.items():
        lines.append(f"{k}: {v}")
    lines.append("<END>")
    return "\n".join(lines) + "\n"

# ---------- CORE SERVER ----------
def broadcast(msg, sender=None):
    """Send LANTP packet to all clients except sender."""
    for user, conn in list(clients.items()):
        if user != sender:
            try:
                conn.send(msg.encode("utf-8"))
            except:
                print(f"⚠️ Lost connection to {user}")
                conn.close()
                clients.pop(user, None)

def handle_client(conn, addr):
    try:
        username = conn.recv(1024).decode().strip()
        if not username:
            conn.close()
            return

        clients[username] = conn
        print(f"[+] {username} connected from {addr}")

        # Notify others
        join_msg = encode_lantp({
            "TYPE": "SYS",
            "FROM": "SERVER",
            "CONTENT": f"{username} joined the chat"
        })
        broadcast(join_msg, sender=username)

        buffer = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode("utf-8")
            while "<END>" in buffer:
                packet, buffer = buffer.split("<END>", 1)
                packet += "<END>"
                msg = decode_lantp(packet)
                if not msg:
                    continue
                if msg["TYPE"] == "MSG":
                    print(f"[MSG] {msg['FROM']}: {msg['CONTENT']}")
                    broadcast(packet, sender=msg["FROM"])

    except Exception as e:
        print(f"⚠️ Error handling client: {e}")
    finally:
        if username in clients:
            print(f"[-] {username} disconnected")
            clients.pop(username, None)
            left_msg = encode_lantp({
                "TYPE": "SYS",
                "FROM": "SERVER",
                "CONTENT": f"{username} left the chat"
            })
            broadcast(left_msg)
        conn.close()

def main():
    lan_ip = get_local_ip()
    print(f"🔵 LANTP/1.0 Server running on {lan_ip}:{PORT}\n")
    print("Clients should connect to the above IP within the same LAN.\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# ---------- MAIN ----------
if __name__ == "__main__":
    main()
