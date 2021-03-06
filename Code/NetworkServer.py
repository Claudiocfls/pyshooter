import Libs.Mastermind as Mastermind
import Code.NetworkSettings as NetworkSettings
import threading
from time import gmtime, strftime

class Server(Mastermind.MastermindServerTCP):
    def __init__(self):
        Mastermind.MastermindServerTCP.__init__(self, 0.5, 0.5, 10.0)  # server refresh, connections' refresh, connection timeout

        self.players = {}
        self.zombies = {}
        self.minimaps = {}
        self.powerups = {}
        self.powerups_states = {}
        self.scores = {}
        self.mutex = threading.Lock()


    def add_player(self, data):
        self.mutex.acquire()
        self.players[data[0]] = data[1][data[0]]
        self.mutex.release()

    def add_minimap(self, data):
        self.mutex.acquire()
        self.minimaps[data[0]] = data[1][data[0]]
        self.mutex.release()

    def add_powerup(self, data):
        self.mutex.acquire()
        self.powerups = data
        self.mutex.release()

    def add_powerup_states(self, data):
        self.mutex.acquire()
        self.powerups_states[data[0]] = data[1]
        self.mutex.release()

    def add_zombie(self, data):
        self.mutex.acquire()
        self.zombies = data
        self.mutex.release()

    def add_scores(self, data):
        self.mutex.acquire()
        self.scores = data
        self.mutex.release()

    def delete_player(self, name):
        self.mutex.acquire()
        self.players.pop(name, None)
        self.minimaps.pop(name, None)
        self.mutex.release()

    def callback_connect(self):
        # Something could go here
        return super(Server, self).callback_connect()

    def callback_disconnect(self):
        # Something could go here
        return super(Server, self).callback_disconnect()

    def callback_connect_client(self, connection_object):
        # Something could go here
        return super(Server, self).callback_connect_client(connection_object)

    def callback_disconnect_client(self, connection_object):
        # Something could go here
        return super(Server, self).callback_disconnect_client(connection_object)

    def callback_client_receive(self, connection_object):
        # Something could go here
        return super(Server, self).callback_client_receive(connection_object)

    def callback_client_handle(self, connection_object, data):
        cmd = data[0]
        if cmd == "player":
            self.add_player(data[1])
            self.callback_client_send(connection_object, ["players", self.players])
        elif cmd == "zombie_host":
            self.add_zombie(data[1])
            self.callback_client_send(connection_object, ["zombies", self.zombies])
        elif cmd == "zombie_client":
            self.callback_client_send(connection_object, ["zombies", self.zombies])
        elif cmd == "powerup_host":
            self.add_powerup(data[1])
            self.callback_client_send(connection_object, ["powerups", self.powerups])
        elif cmd == "powerup_client":
            self.callback_client_send(connection_object, ["powerups", self.powerups])
        elif cmd == "scores_host":
            self.add_scores(data[1])
            self.callback_client_send(connection_object, ["scores", self.scores])
        elif cmd == "scores_client":
            self.callback_client_send(connection_object, ["scores", self.scores])
        elif cmd == "minimaps":
            self.add_minimap(data[1])
            self.callback_client_send(connection_object, ["minimaps", self.minimaps])
        elif cmd == "delete_player":
            self.delete_player(data[1])
            self.callback_client_send(connection_object, ["players", self.players])
        elif cmd == "add_status_player":
            self.add_powerup_states(data[1])
            self.callback_client_send(connection_object, ["powerups_states", self.powerups_states ])


    def callback_client_send(self, connection_object, data, compression=None):
        # Something could go here
        return super(Server, self).callback_client_send(connection_object, data, compression)

if __name__ == "__main__":
    server = Server()
    server.connect(server_ip, port)
    try:
        server.accepting_allow_wait_forever()
    except:
        # Only way to break is with an exception
        pass
    server.accepting_disallow()
    server.disconnect_clients()
    server.disconnect()
