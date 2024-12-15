import socket

HOST = 'localhost'  
PORT = 12345
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connected to the game server.")
        
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode()
            print(message)
            if "Your turn" in message:
                move = input("Enter your move (1-9): ").strip()
                client_socket.send(move.encode())
            if "win" in message or "lose" in message or "draw" in message:
                break

if __name__ == "__main__":
    main()
