import sqlite3

class Database:
    def __init__(self, deb_name='database.db'):
        sel.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
    

    def execute(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql,params or [])
        self.conn.commit()
        return cursor
