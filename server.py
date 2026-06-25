import socket
import ssl
import threading

clients = {}

def handle_client(tls_socket, addr):
    username = None
    try:
        tls_socket.sendall("🔑 ENTER_USERNAME".encode())
        username = tls_socket.recv(1024).decode().strip()
        
        if not username or username in clients:
            tls_socket.sendall("❌ Username invalid ya taken hai. Disconnecting...".encode())
            tls_socket.close()
            return

        clients[username] = tls_socket
        print(f"👤 [JOINED] {username} connected from {addr}")
        tls_socket.sendall(f"✅ Welcome {username}! Private Chat: @user msg | File: @user /send filename\n".encode())

        while True:
            message = tls_socket.recv(1024).decode()
            if not message:
                break
            
            # 1. File Transfer Command Parsing (@username /send filename)
            if message.startswith("@") and " /send " in message:
                try:
                    parts = message.split(" ", 2)
                    target_user = parts[0][1:] # Remove '@'
                    filename = parts[2]

                    if target_user in clients:
                        # Target ko notify karein ke file aa rahi hai
                        clients[target_user].sendall(f"📦 [FILE_COMING] From {username}:{filename}".encode())
                        
                        # Client se raw file size/bytes receive karke direct target ko forward karein
                        tls_socket.sendall("READY_TO_RECEIVE".encode())
                        
                        # File ke bytes stream ko chunk-by-chunk forward karein
                        file_size = int(tls_socket.recv(1024).decode())
                        clients[target_user].sendall(str(file_size).encode())
                        
                        remaining = file_size
                        while remaining > 0:
                            chunk = tls_socket.recv(min(remaining, 4096))
                            if not chunk:
                                break
                            clients[target_user].send(chunk)
                            remaining -= len(chunk)
                            
                        print(f"📁 [FILE] {username} sent '{filename}' to {target_user} successfully.")
                    else:
                        tls_socket.sendall(f"⚠️ User @{target_user} online nahi hai.".encode())
                except Exception as e:
                    print(f"File routing error: {e}")
                    
            # 2. Pehle Wali Standard Private Routing (Unchanged)
            elif message.startswith("@"):
                parts = message.split(" ", 1)
                target_user = parts[0][1:]
                actual_msg = parts[1] if len(parts) > 1 else ""

                if target_user in clients:
                    clients[target_user].sendall(f"🔒 [Private from {username}]: {actual_msg}".encode())
                else:
                    tls_socket.sendall(f"⚠️ User @{target_user} online nahi hai.".encode())
            else:
                tls_socket.sendall("ℹ️ Format: @username message YA @username /send filename".encode())

    except Exception as e:
        print(f"⚠️ Error handling {username or addr}: {e}")
    finally:
        if username in clients:
            del clients[username]
            tls_socket.close()
            print(f"🚪 [LEFT] {username} disconnected.")

# Server Engine Initialization
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 65432))
server_socket.listen(10)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

print("🚀 TLS Private Routing & FTP Server Hub Is Active...")

while True:
    conn, addr = server_socket.accept()
    tls_socket = context.wrap_socket(conn, server_side=True)
    threading.Thread(target=handle_client, args=(tls_socket, addr), daemon=True).start()
