from database.connection import Connection

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connections = {}


    def connection(self, name=None): #Administra las conexiones del frame a la BD
        if not name:
            name = self.config["default"]

        if name not in self.connections:
            self.connections[name] = Connection(self.config[name])
        return self.connections[name]
    
    def _make_connection(self, name):
        conn_config = self.config['connections'][name]

        if conn_config[""] == '':
            return True