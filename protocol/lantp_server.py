import socket
import threading

HOST = "0.0.0.0"
PORT = 5555
clients = {}

def decode_lantp(packet):
    """Parse raw LANTP message into a dict."""
    lines = packet.strip().split("\n")
    if not lines[0].startswith("LANTP/1.0"):
        return None
    data = {}
    for line in lines[1:]:
        if line == "<END>":
            break
        if ": " in line:
            key, val = line.split(": ", 1)
            data[key] = val
    return data

def encode_lantp(data):
    """Convert a dict into LANTP format."""
    lines = ["LANTP/1.0"]
    for k, v in data.items():
        lines.append(f"{k}: {v}")
    lines.append("<END>")
    return "\n".join(lines) + "\n"

def broadcast(msg, sender=None):
    for user, conn in clients.items():
        if user != sender:
            try:
                conn.send(msg.encode("utf-8"))
            except:
                pass

def handle_client(conn, addr):
    username = conn.recv(1024).decode().strip()
    clients[username] = conn
    print(f"[+] {username} connected from {addr}")
    broadcast(encode_lantp({
        "TYPE": "SYS",
        "FROM": "SERVER",
        "CONTENT": f"{username} joined the chat"
    }))
    try:
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
                if msg and msg["TYPE"] == "MSG":
                    print(f"[MSG] {msg['FROM']}: {msg['CONTENT']}")
                    broadcast(packet, sender=msg["FROM"])
    except:
        pass
    finally:
        print(f"[-] {username} disconnected")
        clients.pop(username, None)
        broadcast(encode_lantp({
            "TYPE": "SYS",
            "FROM": "SERVER",
            "CONTENT": f"{username} left the chat"
        }))
        conn.close()

def main():
    print(f"🔵 LANTP/1.0 Server running on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
