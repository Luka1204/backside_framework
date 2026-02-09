from database.query_builder import QueryBuilder
from core.helpers.helpers import app

class Model:
    table = None
    primary_key='id'
    connection_name = 'default'
    
    INTERNAL_ATTRS = {
        'attributes',
        'original',
        'exists',
        'table',
        'primary_key',
        'connection'

    }

    def __init__(self):
        super().__setattr__('attributes',{})
        super().__setattr__('original',{})
        super().__setattr__('exists',False)
        super().__setattr__('connection', None)
    
    def __getattr__(self, key):
        if key in self.attributes:
            return self.attributes.get(key)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __setattr__(self,key,value):
        if key in self.INTERNAL_ATTRS:
            super().__setattr__(key,value)
            return
        self.attributes[key] = value
    
    def get_dirty(self):
        dirty = {}

        for key, value in self.attributes.items():
            if key not in self.original or self.original.get(key) != value:
                dirty[key] = value
        
        return dirty
    @classmethod
    def query(cls):
        db = app().make('db')
        connection = db.connection()
        return QueryBuilder(connection, cls.table)
    
    @classmethod 
    def find(cls, id):
        data = cls.query().where('id',id).first()
        if not data:
            return None
        return cls.hydrate(data)
    
    @classmethod
    def all(cls):
        rows = cls.query().get()
        return [cls.hydrate(row) for row in rows]
    
    @classmethod
    def create(cls, data):
        instance = cls(data)
        instance.save()
        return instance
    
    @classmethod
    def hydrate(cls, data):
        instance = cls(data)
        instance.exists = True
        instance.original = dict(data)
        return instance
    
    def save(self):
        db = app().make('db')
        connection = db.connection()

        if self.exists:
            dirty = self.get_dirty()

            if not dirty:
                return None
            
            columns = []
            bindings = []

            for key, value in self.attributes.items():
                if self.original.get(key) != value:
                    columns.append(f"{key} = %s")
                    bindings.append(value)

            if not columns:
                return None
            
            bindings.append(self.attributes['id'])
            sql = f"UPDATE {self.table} SET {', '.join(columns)} WHERE id = %s"
            connection.execute(sql, bindings)

            self.original.update(dirty)

            return True

        else:
            keys = ', '.join(self.attributes.keys())
            placeholders = ', '.join(['%s'] * len(self.attributes))
            sql = f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})"
            cursor = connection.execute(sql, list(self.attributes.values()))
            self.attributes[self.primary_key] = cursor.lastrowid
            self.exists = True

            self.original = self.attributes.copy()
    

    def delete(self):
        if not self.exists:
            return
        
        db= app().make('db')
        connection = db.connection()
        connection.execute(f"DELETE FROM {self.table} WHERE id = %s",
        [self.attributes['id']])
        self.exists = False
    
    def to_dict(self):
        return self.attributes