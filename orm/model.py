class Model:
    table = None
    db = None

    @classmethod
    def set_database(cls, database):
        cls.db = database
    
    @classmethod
    def all(cls):
        result = cls.db.execute(f'SELECT * FROM {cls.table}')
        return [dict(row) for row in result.fetchall()]
    
    @classmethod
    def find(cls, id):
        result = cls.db.execute(f'SELECT * FROM {cls.table} WHERE id = %s', [id])
        row = result.fetchone()
        return dict(row) if row else None