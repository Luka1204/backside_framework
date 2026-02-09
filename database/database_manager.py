from database.connection import Connection

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connections = {}


    def connection(self, name='default'): #Administra las conexiones del frame a la BD
        if name not in self.connections:
            self.connections[name] = Connection(self.config[name])
        return self.connections[name]