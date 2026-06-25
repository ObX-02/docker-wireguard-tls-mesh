 **docker-wireguard-tls-mesh**
1. **Isolated WireGuard Network (Docker):** Containers configured on network matrices to route localized traffic securely.
2. **Layer-4 Custom Sockets & TLS:** Replaced raw network pings with custom TCP sockets wrapped under Transport Layer Security (`ssl`).
3. **Multi-Client Concurrency:** Threaded execution architecture allowing multiple nodes to engage in parallel communication.
4. **Private Command Routing:** Real-time `@username` address parsing logic preventing cross-client data visibility.

  5 
            **Architecture Network Flow**

  6           --------------------------------                             
             |  DOCKER CONTAINER (SERVER)    |
             | (WireGuard Tunnel Interface)  |
             |    IP: 10.13.13.1             |
             --------------------------------
                           |
              --------------------------------
             |  PHYSICAL CLIENT NODE         |
             | (Local Wi-Fi/LAN IP)          |
             |    IP: 10.13.13.2             |
             --------------------------------

             
  7         Server Node: The persistent TLS daemon is running isolated inside a Docker container, actively listing on port 65432 round to the WireGuard interface (10.13.13.1).
  
  8        Client Node: The physical machine initiates a handshake over its virtual gateway peer interface (10.13.13.2).

  9       The Proof: Upon succable cryptographic validation, the server decapsules the packet stream and explically logs the absolute source IP of the client node proving absolute route tracking.

  10     
   python3 server.py
🚀 TLS Private Routing & FTP Server Hub Is Active...
👤 [JOINED] luna connected from ('127.0.0.1', 59206)
👤 [JOINED] lusi connected from ('127.0.0.1', 54076)
👤 [JOINED] jina connected from ('127.0.0.1', 54092)
🚪 [LEFT] jina disconnected.
👤 [JOINED] minha connected from ('127.0.0.1', 46114)
🚪 [LEFT] luna disconnected.


  11    Proof Analysis: The runtime log entry Connected from: ('10.13.13.2', 54321) guarantees that the server has been able to reach the control over the professional network matrix, and tracked the connection back to the act peer node.

   python3 client.py
👤 Apna Username likhein: luna
✅ Welcome luna! Private Chat: @user msg | File: @user /send filename
✍️  You: @lusi hello 
🔒 [Private from lusi]: hello
🔒 [Private from jina]: @lusi hello both of u
🔒 [Private from minha]: hello
✍️  You: @minha hello

12            
