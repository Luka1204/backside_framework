import sqlite3

class Connection:
    def connect(self):
        raise NotImplementedError
    
    def execute(self,query,bindings=None):
        raise NotImplementedError
    
    def select(self,query,bindings=None):
        raise NotImplementedError
    
    def insert(self,query,bindings=None):
        raise NotImplementedError
    
    def update(self,query,bindings=None):
        raise NotImplementedError
    
    def delete(self,query,bindings=None):
        raise NotImplementedError
    
    def last_insert_id(self):
        raise NotImplementedError
