import socket
import random
import datetime

# Definice citátů
quotes = [
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "In the middle of difficulty lies opportunity. - Albert Einstein",
    "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "Life is what happens when you're busy making other plans. - John Lennon"
]

# Funkce pro zpracování příkazů
def handle_command(command):
    if command == "quote":
        return random.choice(quotes) + "\n"
    elif command == "date":
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    elif command == "help":
        return "Available commands:\n - quote\n - date\n - help\n - exit\n - shutdown-server\n"
    elif command == "exit":
        return "Goodbye!\n"
    elif command == "shutdown-server":
        return "Shutting down server...\n"
    else:
        return "Unknown command. Type 'help' for a list of commands.\n"

# Nastavení serveru
server_address = ("192.168.68.100", 65532)  # Použijte svou IP adresu

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(server_address)
    server_socket.listen()
    print(f"Server started on {server_address[0]}:{server_address[1]}")

    shutdown = False  # Stav serveru

    while not shutdown:  # Hlavní smyčka serveru
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        with connection:
            print(f"Connected to {client_address[0]}:{client_address[1]}")

            buffer = ""  # Buffer pro příchozí data
            while not shutdown:  # Smyčka zpracovávající příkazy klienta
                try:
                    # Přijímání dat od klienta
                    data = connection.recv(1024).decode("utf-8")
                    if not data:
                        print(f"Connection with {client_address[0]}:{client_address[1]} closed")
                        break

                    buffer += data  # Přidání přijatých dat do bufferu

                    # Zpracování kompletního příkazu (na základě \r\n z PuTTY)
                    while "\r\n" in buffer:
                        command, buffer = buffer.split("\r\n", 1)
                        command = command.strip().lower()  # Odstranění mezer a malá písmena
                        print(f"Received command: {command}")

                        # Zpracování příkazu
                        response = handle_command(command)
                        connection.send(response.encode("utf-8"))

                        # Speciální příkazy
                        if command == "exit":
                            print(f"Client {client_address[0]}:{client_address[1]} disconnected")
                            break
                        elif command == "shutdown-server":
                            print("Server is shutting down...")
                            shutdown = True  # Nastavení příznaku ukončení
                            break

                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        # Ukončení hlavní smyčky při shutdown
        if shutdown:
            break

    print("Server has been shut down.")
