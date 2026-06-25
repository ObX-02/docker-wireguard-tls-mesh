# Secure TLS Multi-Client Chat,  WireGuard VPN Infrastructure

A production-grade implementation of an isolated, secure networking environment. This project demonstrates local cloud security by layering asymmetric cryptography (TLS), multi-client concurrency (Threading), and custom secure file transfer protocols, designed to run within a Dockerized WireGuard VPN wrapper.

---

## 🛠️ Infrastructure Core Features

* **Isolated WireGuard Network (Docker):** Containers configured on custom network matrices to route localized traffic securely.
* **Layer-4 Custom Sockets & TLS:** Replaced raw network pings with custom TCP sockets wrapped under Transport Layer Security (`ssl`).
* **Multi-Client Concurrency:** Threaded execution architecture allowing multiple nodes to engage in parallel communication.
* **Private Command Routing:** Real-time `@username` address parsing logic preventing cross-client data visibility.
* **Secure FTP Layer:** Handshakes engineered to split binary byte-streams (`rb`/`wb`) to deliver encrypted file payloads over the TLS tunnel.

---

## 🗺️ Architectural Network Flow

```text
┌────────────────────────────────┐               ┌────────────────────────────────┐
│    DOCKER CONTAINER (SERVER)   │               │     PHYSICAL CLIENT NODE       │
│  (WireGuard Tunnel Interface)  │ ◄───────────► │      (Local Wi-Fi/LAN IP)      │
│       IP: 10.13.13.1           │               │       IP: 10.13.13.2           │
└────────────────────────────────┘               └────────────────────────────────┘
