import socket
import threading
import sys

SERVER_IP = "127.0.0.1"  # change if server is remote
SERVER_PORT = 5555       # must match server_config.json

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                print("\n[Disconnected from server]")
                break
            print("\n" + data.strip())
            print("> ", end="", flush=True)
        except:
            break

def main():
    print("=== LAN Chat Client ===")
    ip = input(f"Server IP [{SERVER_IP}]: ").strip() or SERVER_IP
    port_in = input(f"Port [{SERVER_PORT}]: ").strip()
    port = int(port_in) if port_in else SERVER_PORT

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
    except Exception as e:
        print("❌ Connection failed:", e)
        return

    print("✅ Connected to server.")
    print(sock.recv(1024).decode())  # welcome message

    # login/signup phase
    while True:
        cmd = input("> ").strip()
        sock.send((cmd + "\n").encode())
        resp = sock.recv(1024).decode()
        print(resp.strip())
        if "Welcome," in resp or "Login successful" in resp:
            break
        if "Goodbye" in resp or not resp:
            sock.close()
            return

    # start receiving thread
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # main chat loop
    try:
        while True:
            msg = input("> ").strip()
            if not msg:
                continue
            sock.send((msg + "\n").encode())
            if msg.lower() == "/exit":
                break
    except KeyboardInterrupt:
        pass
    finally:
        print("\n👋 Disconnected.")
        sock.close()

if __name__ == "__main__":
    main()
