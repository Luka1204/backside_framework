import sqlite3
from database.connection import Connection

class SQLiteConnection(Connection):
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.config['database'])
            self.connection.row2_factory = sqlite3.Row
        
    def execute(self, query, bindings=None):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, bindings or [])
        self.connection.commit()
        return cursor
    
    def select(self, query, bindings=None):
        cursor = self.execute(query, bindings)
        return [dict(row) for row in cursor.fetchall()]
    
    def last_insert_id(self):
        return self.connection.cursor().lastrowid