import socket
import threading


HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

class GameSession(threading.Thread):
    def __init__(self, player1, player2):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.board = [' ' for _ in range(9)]
        self.current_player = 1
    
    def run(self):

        self.player1.send(b"You are Player 1 (X). Waiting for Player 2...")
        self.player2.send(b"You are Player 2 (O). Game starting now!")
        
        # Game loop
        while True:

            self.send_board()
            

            player = self.player1 if self.current_player == 1 else self.player2
            token = 'X' if self.current_player == 1 else 'O'


            player.send(b"Your turn. Enter a position (1-9): ")
            move = player.recv(BUFFER_SIZE).decode().strip()
            
            if not move.isdigit() or int(move) not in range(1, 10):
                player.send(b"Invalid input. Try again.")
                continue
            
            position = int(move) - 1
            if self.board[position] != ' ':
                player.send(b"Position already taken. Try again.")
                continue


            self.board[position] = token


            if self.check_winner(token):
                self.send_board()
                player.send(b"You win!")
                (self.player1 if self.current_player != 1 else self.player2).send(b"You lose!")
                break
            elif ' ' not in self.board:
                self.send_board()
                self.player1.send(b"It's a draw!")
                self.player2.send(b"It's a draw!")
                break
            

            self.current_player = 2 if self.current_player == 1 else 1

        self.player1.close()
        self.player2.close()

    def send_board(self):
        board_view = "\n".join([
            f"{self.board[0]} | {self.board[1]} | {self.board[2]}",
            "---------",
            f"{self.board[3]} | {self.board[4]} | {self.board[5]}",
            "---------",
            f"{self.board[6]} | {self.board[7]} | {self.board[8]}",
        ])
        self.player1.send(board_view.encode())
        self.player2.send(board_view.encode())
    
    def check_winner(self, token):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6],            
        ]
        return any(all(self.board[pos] == token for pos in condition) for condition in win_conditions)

def accept_clients(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")
        if len(connected_players) % 2 == 0:
            connected_players.append(client_socket)
            client_socket.send(b"Waiting for Player 2 to connect...")
        else:
            connected_players.append(client_socket)
            player1 = connected_players[-2]
            player2 = connected_players[-1]
            print(f"Starting a new game session: {player1.getpeername()} vs {player2.getpeername()}")
            game_session = GameSession(player1, player2)
            game_session.start()

if __name__ == "__main__":
    connected_players = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")
        accept_clients(server_socket)
