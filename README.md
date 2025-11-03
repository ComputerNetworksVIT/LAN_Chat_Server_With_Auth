# LAN_Chat_Server_With_Auth
24BCE1964 Bashar Mohammad Wakil

---

````markdown
# 💬 LAN Chat Server with Authentication & Admin Controls

A **real-time LAN chat system** built using **Python sockets**, designed for **authenticated multi-user communication** with **admin moderation tools**.  
This project is part of a **Computer Networks (CN) course project**, implementing a **custom server-client architecture** that runs purely in the terminal for simplicity and transparency.

---

## 🚀 Overview

The **LAN Chat Server** enables multiple users on the same network to chat through a centralized server.  
Admins can manage connected users through moderation commands such as **kick**, **mute**, **ban**, and **broadcast**, while regular users can chat globally or send **private messages** using `@username`.

The project also lays groundwork for a **custom STP (Simple Transmission Protocol)** layer to standardize packet structures and message handling between server and clients.

---

## ✨ Features

- 🔐 **User Authentication** (username/password)
- 🧩 **Role System** – Admins and Regular Users
- 💬 **Global Chat + Private Messaging**
- 🚫 **Admin Commands**
  - `/kick <user> [reason]`
  - `/mute <user> [minutes]`
  - `/unmute <user>`
  - `/ban <user> [minutes]`
  - `/unban <user>`
  - `/broadcast <message>`
- 👀 **Active User List** and Join/Leave Notifications
- 🧵 **Multi-threaded Communication**
- 🧱 **Console-Based and Lightweight**
- 🧠 **Extensible Protocol (STP) under development**

---

## 🗂️ Folder Structure

```bash
LAN_Chat_Server_With_Auth/
│
├── server/
│   └── server.py
│
├── client/
│   └── client.py
│
└── README.md
````

---

## ⚙️ Installation & Setup

### 🪟 For Windows

1. **Install Python 3.12+**

   * Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
   * During installation, check ✅ *“Add Python to PATH”*

2. **Clone the Repository**

   ```bash
   git clone https://github.com/ComputerNetworksVIT/LAN_Chat_Server_With_Auth.git
   cd LAN_Chat_Server_With_Auth
   ```

3. **Run the Server**

   ```bash
   cd server
   python server.py
   ```

4. **Run the Client**

   ```bash
   cd client
   python client.py
   ```

---

## 🧠 Command Reference

| Command                  | Description                    | Role  |
| ------------------------ | ------------------------------ | ----- |
| `/help`                  | Display all available commands | All   |
| `/users`                 | List currently online users    | All   |
| `@username <msg>`        | Send private message           | All   |
| `/kick <user> [reason]`  | Kick a user from the chat      | Admin |
| `/mute <user> [minutes]` | Temporarily mute a user        | Admin |
| `/unmute <user>`         | Remove mute restriction        | Admin |
| `/ban <user> [minutes]`  | Temporarily ban login          | Admin |
| `/unban <user>`          | Remove ban restriction         | Admin |
| `/broadcast <msg>`       | Send server-wide announcement  | Admin |

---

## 🧪 Example Session

```
[Server] Listening on 0.0.0.0:5000
📥 User 'alex' joined the chat.
📥 [Admin] 'root' joined the chat.
[Admin] root: /mute alex 2
🔇 alex was muted by an admin for 2 minute(s).
alex: test
🚫 You are muted.
```

---

## 🧱 Tech Stack

| Component     | Technology        |
| ------------- | ----------------- |
| Language      | Python 3          |
| Networking    | Socket, Threading |
| Architecture  | Client-Server     |
| Protocol Plan | STP (custom, WIP) |

---

## 🧩 Future Enhancements

* 📡 Implementation of **STP (Simple Transmission Protocol)** for structured messaging (Custom Protocol)
* 💾 **Chat Logs** and `/whois` command to check user status
* 🧠 Persistent storage for user roles and bans
* 🪟 Optional GUI Client (Tkinter or PyQt)
* 🔔 Notification system for mentions and PMs

---

## 👥 Author

Developed by **Bashar Mohammad Wakil 24BCE1964** as part of a Computer Networks (CN) B.Tech project
---

