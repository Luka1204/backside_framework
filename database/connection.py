import sqlite3

class Connection:
    def __init__(self, config):        
        self.conn = config
        self._connection = None

    def connect(self):
        if not self._connection: # Si no existe conexion la crea
            self.connection = sqlite3.connect(self.config['database'])
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def execute(self, query, bindings=None):
        bindings = bindings or []
        cursor = self.connect().cursor()
        cursor.execute(query, bindings)
        self.connect().commit()
        return cursor
