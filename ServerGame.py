import socket
import threading


class PlayerHandler(threading.Thread):
    def __init__(self, conn, addr, gameserver):
        super(PlayerHandler, self).__init__()
        self.conn = conn
        self.addr = addr
        self.running = True
        self.gameserver = gameserver

    def handle_data(self, data):
        message = data.decode("utf-8")
        print(f"Received message from {self.addr}: {message}")
        if message == "Disconnecting":
            self.gameserver.disconnect_client(self.conn, self.addr)
            self.running = False

    def send_data(self, data):
        self.conn.send(data)

    def run(self):
        print(f"Player connected: {self.addr}")
        while self.running:
            try:
                data = self.conn.recv(1024)
                if data:
                    self.handle_data(data)
                # Send response to client
                #response = "Response from server"
                # self.conn.send(response.encode("utf-8"))
            except Exception as e:
                print(f"Error handling data from {self.addr}: {e}")
                self.gameserver.disconnect_client(self.conn, self.addr)
                break

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = False
        self.player_count = 0
        self.player_handlers = []

    def start_server(self):
        self.running = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(2)
            print(f"Server listening on {self.host}:{self.port}")

            while self.running:
                # Wait for a client to connect
                conn, addr = s.accept()

                # Check if maximum player count has been reached
                if self.player_count >= 2:
                    conn.send("server is Full".encode())
                    conn.close()
                    continue

                # Handle new player
                player_handler = PlayerHandler(conn, addr, self)
                self.player_handlers.append(player_handler)
                player_handler.start()
                self.player_count += 1

                print(f"Player count: {self.player_count}")

                # Check if maximum player count has been reached
                if self.player_count >= 2:
                    print("Server is full")
                    return True

                #play_game(self.player_handlers[0].conn, self.player_handlers[1].conn)

    def stop(self):
        self.running = False
        for player_handler in self.player_handlers:
            player_handler.running = False
            player_handler.join()
        print("Server stopped")

    def disconnect_client(self, conn, addr):
        print(f"Player {self.player_count} disconnected: {addr}")
        self.player_count -= 1
        conn.close()

class GameServer(Server):

    def start_game(self):
        super().start_server()
        while self.running:
            # do game logic

            # first start by loading the screen

            # than chose the firest player that should play by randomness
            # than start the game logic
            pass


if __name__ == "__main__":
    game_server = GameServer("127.0.0.1", 25001)
    game_server.start_game()
