import socket

HOST = "127.0.0.1"
PORT = 12345

mode = input("Choose mode (server/client): ").lower()

if mode == "server":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("Waiting for client connection...")

    conn, addr = server.accept()
    print(f"Connected to {addr}")

    while True:
        msg = conn.recv(1024).decode()

        if not msg or msg.lower() == "exit":
            print("Client disconnected.")
            break

        print(f"\nClient: {msg}")

        reply = input("You: ")
        conn.send(reply.encode())

        if reply.lower() == "exit":
            break

    conn.close()
    server.close()

elif mode == "client":

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print("Connected to server.")

        while True:
            msg = input("You: ")
            client.send(msg.encode())

            if msg.lower() == "exit":
                break

            reply = client.recv(1024).decode()

            if not reply or reply.lower() == "exit":
                print("Server disconnected.")
                break

            print(f"\nServer: {reply}")

        client.close()

    except ConnectionRefusedError:
        print("Server is not running.")

else:
    print("Invalid mode. Choose 'server' or 'client'.")



