import socket

GRID_SIZE = 10, 10

ID = 1

HOST = '127.0.0.1'
PORT = 5000

def Initialize_networking():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
# Unit class for game objects


class Unit:
    def __init__(self, pos, color, unit_type):
        self.pos = pos
        self.color = color
        self.unit_type = unit_type
        self.id = ID
        ID += 1

    def move(self, pos):
        self.pos = pos

    def attack(self, attack_type, other_player_unit):
        # do  damage to other player
        pass

# Game class to manage the game state and logic


class Game:
    def __init__(self):
        self.units = []
        self.players = []
        self.current_player = None

    def add_player(self, player):
        self.players.append(player)

    def add_unit(self, unit):
        self.units.append(unit)

    def get_current_player(self):
        return self.current_player

    def set_current_player(self, player):
        self.current_player = player

    def handle_events(self):
        # start with random player
        # player select unity =>self.current_player.select_unit(unit)
        # select action move or attack other player
        # commit that action
        pass

    def update(self):
        # get data
        for player in self.players:
            player.socket.send(data)

# Player class to manage player state


class Player:
    def __init__(self, socket, id):
        self.socket = socket
        self.selected_unit = None
        self.units = []
        self.id = id

    def select_unit(self, unit):
        self.selected_unit = unit

    def get_selected_unit(self):
        return self.selected_unit

    def add_unit(self, pos, color, unit_type):
        unit = Unit(pos, color, unit_type)
        self.units.append(unit)

# Main game loop


def game_loop(game):
    while True:
        game.handle_events()
        game.update()

        # Receive data from clients
        conn, addr = server_socket.accept()
        data = conn.recv(4096)
        if not data:
            break

        # Update game state from data
        # do main  loop
        conn.close()


def Game_setup():
    game = Game()
    player1 = Player(None, game.players.__len__()+1)
    game.add_player(player1)
    player2 = Player(None, game.players.__len__()+1)
    game.add_player(player2)

if __name__ == "__main__":
    Game_setup()
