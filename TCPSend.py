import socket

# Definujeme IP adresu a port, na kterém bude server naslouchat
server_inet_address = ("127.0.0.1", 65532)

# Vytvoříme socket a provedeme bind
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(server_inet_address)
    server_socket.listen()
    print(f"Server started on {server_inet_address[0]}:{server_inet_address[1]}")

    try:
        # Server čeká na příchozí připojení
        while True:
            print("Waiting for a connection...")
            connection, client_inet_address = server_socket.accept()
            with connection:
                print(f"Connection accepted from {client_inet_address[0]}:{client_inet_address[1]}")

                # Zpráva pro klienta
                message = "HELLOM\n"
                message_as_bytes = bytes(message, "utf-8")
                connection.send(message_as_bytes)
                print("Message sent to the client")

                # Připojení ukončeno
                print(f"Connection with {client_inet_address[0]}:{client_inet_address[1]} closed")
    except KeyboardInterrupt:
        print("\nServer stopped manually")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Server is shutting down")
