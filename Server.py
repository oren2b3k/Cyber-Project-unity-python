import socket
import threading
import random
import atexit
import game

PORT_IP = ("127.0.0.1", 25001)


class PlayerHandler(threading.Thread):
    def __init__(self, conn, addr, player_num, game_server):
        super(PlayerHandler, self).__init__()
        self.conn = conn
        self.addr = addr
        self.player_num = player_num
        self.game_server = game_server
        self.running = True

    def handle_data(self, data):
        message = data.decode("utf-8")
        print(f"Received message from {self.addr}: {message}")
        if message.startswith("Disconnecting"):
            if not self.conn._closed:
                self.game_server.disconnect_client(self)
        # handle message

    def send_data(self, data):
        self.conn.send(data.encode())

    def run(self):
        print(f"Player {self.player_num} connected: {self.addr}")
        while self.running:
            try:
                data = self.conn.recv(1024)
                if data:
                    self.handle_data(data)
            except Exception as e:
                self.running = False
                if not self.conn._closed:
                    print(f"Error handling data from {self.addr}: {e}")
                    return
                self.game_server.disconnect_client(self)


def send_shutdown_message(player_handlers):
    for player_handler in player_handlers:
        if not player_handler.conn._closed:
            player_handler.send_data("Server is shutting down")
    print("Server is shutting down")


class Server:
    def __init__(self):
        self.player_count = 0
        self.player_handlers = []
        self.running = False

    def start_server(self):
        self.running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(PORT_IP)
            s.listen(2)
            print(f"Server listening on 127.0.0.1 : 25001")

            while self.running:
                # Wait for a client to connect
                conn, addr = s.accept()

                # Check if maximum player count has been reached
                if self.player_count >= 2:
                    conn.send("server is Full".encode())
                    conn.close()
                    continue

                # Handle new player
                self.player_count += 1
                player_handler = PlayerHandler(
                    conn, addr, self.player_count, self)
                self.player_handlers.append(player_handler)
                player_handler.start()

                print(f"Player id of current player: {self.player_count}")

                # Check if maximum player count has been reached
                if self.player_count >= 2:
                    print("Server is full and ready to start")
                    self.playing_game = True
                    return

    def stop(self):
        self.running = False
        send_shutdown_message(self.player_handlers)
        [player_handler.join() for player_handler in self.player_handlers]
        print("Server stopped")

    def disconnect_client(self, player_handler):
        if player_handler.conn._closed:
            return
        print(
            f"Player {self.player_count} disconnected: {player_handler.addr}")
        self.player_count -= 1
        player_handler.conn.close()
        self.player_handlers.remove(player_handler)
        if self.playing_game:
            self.playing_game = False
            self.start_server()
