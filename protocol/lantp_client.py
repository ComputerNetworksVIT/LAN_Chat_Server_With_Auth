import socket
import threading

SERVER_IP = input("Enter server IP: ").strip()
PORT = 5555
username = input("Enter your username: ").strip()

def encode_lantp(data):
    lines = ["LANTP/1.0"]
    for k, v in data.items():
        lines.append(f"{k}: {v}")
    lines.append("<END>")
    return "\n".join(lines) + "\n"

def recv_messages(sock):
    buffer = ""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            buffer += data.decode("utf-8")
            while "<END>" in buffer:
                packet, buffer = buffer.split("<END>", 1)
                packet += "<END>"
                print("\n" + packet.strip() + "\n> ", end="")
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, PORT))
    s.send(username.encode())
    threading.Thread(target=recv_messages, args=(s,), daemon=True).start()

    while True:
        msg = input("> ")
        if msg.lower() == "/quit":
            break
        packet = encode_lantp({
            "TYPE": "MSG",
            "FROM": username,
            "CONTENT": msg
        })
        s.send(packet.encode("utf-8"))
