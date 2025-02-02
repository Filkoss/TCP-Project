import socket
import threading

class ClientApp:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.running = True

    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            print(f"Connected to server {self.server_ip}:{self.server_port}")
        except Exception as e:  
            print(f"Failed to connect to server: {e}")
            self.running = False

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode("utf-8"))
        except Exception as e:
            print(f"Error sending message: {e}")
            self.running = False

    def receive_messages(self):
        try:
            while self.running:
                response = self.socket.recv(1024).decode("utf-8")
                if not response:
                    print("Disconnected from server.")
                    break
                print(f"SERVER> {response.strip()}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            self.running = False

    def start(self):
        self.connect_to_server()
        if not self.running:
            return

        # Spustí vlákno pro příjem zpráv ze serveru
        threading.Thread(target=self.receive_messages, daemon=True).start()

        print("Type your messages below (type 'exit' to quit):")
        while self.running:
            message = input("> ")
            if message.lower() == "exit":
                self.running = False
                self.send_message("exit")
                print("Exiting client...")
                break
            elif message.strip():  # Zajistí, že prázdné zprávy se neodesílají
                self.send_message(message)

        self.socket.close()

if __name__ == "__main__":
    server_ip = input("Enter server IP (e.g., 127.0.0.1): ")
    server_port = int(input("Enter server port (e.g., 65532): "))

    client = ClientApp(server_ip, server_port)
    client.start()
