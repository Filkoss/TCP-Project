import socket
import threading
import random
import datetime

# Definice citátů
quotes = [
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "In the middle of difficulty lies opportunity. - Albert Einstein",
    "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "Life is what happens when you're busy making other plans. - John Lennon"
]

# Globální seznam připojených klientů
clients = []
lock = threading.Lock()  # Zámek pro synchronizaci přístupu ke sdíleným datům
shutdown_votes = {}  # Sledování hlasování o vypnutí serveru


# Funkce pro zpracování příkazů
def handle_command(command, connection, client_address):
    global shutdown_votes
    if command == "quote":
        return random.choice(quotes) + "\n"
    elif command == "date":
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    elif command == "help":
        return "Available commands:\n - quote\n - date\n - help\n - clients\n - broadcast <message>\n - shutdown-server\n - exit\n"
    elif command == "clients":
        return f"Currently connected clients: {len(clients)}\n"
    elif command.startswith("broadcast"):
        _, message = command.split(" ", 1)
        broadcast_message(f"Broadcast from {client_address[0]}:{client_address[1]}: {message}")
        return "Broadcast message sent.\n"
    elif command == "shutdown-server":
        shutdown_votes[client_address] = True
        if len(shutdown_votes) == len(clients):
            broadcast_message("Server is shutting down...")
            return "Server is shutting down...\n", True  # Vracení příznaku vypnutí
        else:
            return "Waiting for all clients to confirm shutdown...\n"
    elif command == "exit":
        return "Goodbye!\n"
    else:
        return "Unknown command. Type 'help' for a list of commands.\n"


# Funkce pro broadcast zprávu
def broadcast_message(message):
    with lock:
        for client in clients:
            try:
                client["connection"].send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error sending broadcast to {client['address']}: {e}")


# Funkce pro obsluhu klienta
def client_handler(connection, client_address):
    global shutdown_votes
    print(f"Client {client_address[0]}:{client_address[1]} connected.")
    clients.append({"connection": connection, "address": client_address})

    try:
        while True:
            data = connection.recv(1024).decode("utf-8").strip()
            if not data:
                break

            print(f"Received command from {client_address}: {data}")
            response = handle_command(data, connection, client_address)

            # Pokud příkaz vrací více hodnot, zpracuj příznak vypnutí
            if isinstance(response, tuple):
                response, shutdown = response
                if shutdown:
                    break

            connection.send(response.encode("utf-8"))

            if data == "exit":
                break
    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        print(f"Client {client_address[0]}:{client_address[1]} disconnected.")
        with lock:
            clients.remove({"connection": connection, "address": client_address})
            if client_address in shutdown_votes:
                del shutdown_votes[client_address]
        connection.close()


# Nastavení serveru
def start_server():
    server_address = ("192.168.68.100", 65532)  # Použijte svou IP adresu

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen()
        print(f"Server started on {server_address[0]}:{server_address[1]}")

        while True:
            print("Waiting for a connection...")
            connection, client_address = server_socket.accept()
            threading.Thread(target=client_handler, args=(connection, client_address)).start()


if __name__ == "__main__":
    start_server()
