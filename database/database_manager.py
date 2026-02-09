from database.connection import Connection

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connections = {}


    def connection(self, name=None): #Administra las conexiones del frame a la BD
        name = name or self.config['default']

        if name in self.connections:
            return self.connections[name]
        connection_config = self.config['connections'].get(name)
        if not connection_config:
            raise Exception(f"Database connection [{name}] not configured")

        driver = connection_config['driver']
        from database.connection_factory import ConnectionFactory

        connection = ConnectionFactory.make(driver, connection_config)
        self.connections[name] = connection
        return connection
    
    def _make_connection(self, name):
        conn_config = self.config['connections'][name]

        if conn_config[""] == '':
            return True