import pymysql
from database.connection import Connection

class MySQLConnection(Connection):
    placeholder = '%s'

    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def connect(self):
        if self.connection:
            return 
        
        self.connection = pymysql.connect(
            host=self.config.get('host','localhost'),
            port=self.config.get('port', 3306),
            user=self.config.get('username'),
            password=self.config.get('password'),
            database=self.config.get('database'),
            charset=self.config.get('charset','utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    
    def execute(self, query, bindings=None):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, bindings or [])
        self.connection.commit()
        return cursor
        
    def select(self, query, bindings=None):
        cursor = self.execute(query,bindings)
        return cursor.fetchall()
    
    def insert(self, query, bindings=None):
        return self.execute(query, bindings)
    
    def update(self, query, bindings=None):
        return self.execute(query, bindings)
    
    def delete(self, query, bindings=None):
        return self.execute(query, bindings)
    
    def last_insert_id(self):
        return self.connection.insert_id