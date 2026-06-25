import socket
import ssl
import threading
import sys
import os

def receive_messages(tls_client):
    while True:
        try:
            message = tls_client.recv(1024).decode()
            if not message:
                break
                
            if message == "🔑 ENTER_USERNAME":
                continue
                
            # Incoming File handling
            if message.startswith("📦 [FILE_COMING]"):
                parts = message.split(":", 1)
                info = parts[0]
                filename = "recv_" + parts[1] # Prefixed to avoid overwriting local files
                
                print(f"\r\n📥 {info}. Receiving file as '{filename}'...")
                
                # File size aur binary chunks receive karein
                file_size = int(tls_client.recv(1024).decode())
                
                with open(filename, "wb") as f:
                    remaining = file_size
                    while remaining > 0:
                        chunk = tls_client.recv(min(remaining, 4096))
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)
                        
                print(f"💾 File successfully saved as '{filename}'!\n✍️  You: ", end="")
                sys.stdout.flush()
                
            else:
                print(f"\r{message}\n✍️  You: ", end="")
                sys.stdout.flush()
        except:
            break

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection(('127.0.0.1', 65432)) as sock:
    with context.wrap_socket(sock, server_hostname='localhost') as tls_client:
        
        my_username = input("👤 Apna Username likhein: ").strip()
        tls_client.sendall(my_username.encode())

        threading.Thread(target=receive_messages, args=(tls_client,), daemon=True).start()
        
        while True:
            try:
                msg = input("✍️  You: ")
                if msg.lower() == 'quit':
                    break
                    
                if msg.strip():
                    # Check agar user file bhejna chahta hai
                    if msg.startswith("@") and " /send " in msg:
                        try:
                            parts = msg.split(" ", 2)
                            filepath = parts[2]
                            
                            if os.path.exists(filepath):
                                # 1. Server ko notification bhejen
                                tls_client.sendall(msg.encode())
                                
                                # Server ke ready hone ka wait karein
                                response = tls_client.recv(1024).decode()
                                if response == "READY_TO_RECEIVE":
                                    file_size = os.path.getsize(filepath)
                                    tls_client.sendall(str(file_size).encode())
                                    
                                    # 2. File ko binary mode mein read karke transmit karein
                                    with open(filepath, "rb") as f:
                                        while (chunk := f.read(4096)):
                                            tls_client.sendall(chunk)
                                    print("📤 File transmission completed!")
                            else:
                                print("⚠️ Error: File path sahi nahi hai.")
                        except Exception as e:
                            print(f"⚠️ Transmission failed: {e}")
                    else:
                        # Normal text routing (Unchanged)
                        tls_client.sendall(msg.encode())
            except (KeyboardInterrupt, EOFError):
                break
