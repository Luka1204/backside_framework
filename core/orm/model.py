from database.query_builder import QueryBuilder
from core.helpers.helpers import app
from datetime import datetime

from core.orm.relations.belongs_to import BelongsTo
from core.orm.relations.has_many import HasMany
from core.orm.relations.has_one import HasOne
from core.orm.relations.belongs_to_many import BelognsToMany

class Model:
    table = None
    primary_key='id'
    connection_name = 'default'

    fillable=[]
    guarded = ['id']
    casts = {}

    
    INTERNAL_ATTRS = {
        'attributes',
        'original',
        'exists',
        'table',
        'primary_key',
        'connection'

    }

    def __init__(self,data = None):
        super().__setattr__('attributes',{})
        super().__setattr__('original',{})
        super().__setattr__('exists',False)
        super().__setattr__('connection', None)

        if data:
            self.fill(data)

    def fill(self, data:dict):
        for key, value in data.items():
            if key in self.INTERNAL_ATTRS:
                continue

            if self.fillable and key not in self.fillable:
                continue

            if self.guarded and key in self.guarded:
                continue

            self.attributes[key] = value

    
    def __getattr__(self, key):
        if key in self.attributes:
            return self.attributes.get(key)
        
        if hasattr(self, key):
            relation=getattr(self, key)()
            self.attributes[key] = relation
            return relation
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __setattr__(self,key,value):
        if key in self.INTERNAL_ATTRS:
            super().__setattr__(key,value)
            return
        self.attributes[key] = value

    def cast_attribute(self, key, value):
        if key not in self.casts or value is None:
            return value
        
        cast = self.casts[key]

        try:
            if cast is int:
                return int(value)
            if cast is float:
                return float(value)
            if cast is bool:
                return bool(int(value))
            if cast == 'datetime':
                return datetime.fromisoformat(value)
        except Exception:
            return value
        
        return value
    
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
        return QueryBuilder(connection, cls.table, cls)
    
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
            
            ph = connection.placeholder
            
            columns = [f"{k} = {ph}" for k in dirty]
            bindings = list(dirty.values()) + [self.attributes[self.primary_key]]

            sql = f"UPDATE {self.table} SET {', '.join(columns)} WHERE {self.primary_key} = {ph}"
            connection.execute(sql, bindings)

            self.original.update(dirty)

            return True

        else:
            keys = list(self.attributes.keys())
            ph = connection.placeholder
            placeholders = ', '.join([ph] * len(keys))

            sql = f"INSERT INTO {self.table} ({', '.join(keys)}) VALUES ({placeholders})"
            cursor = connection.execute(sql, list(self.attributes.values()))

            self.attributes[self.primary_key] = cursor.lastrowid
            self.original = dict(self.attributes)
            self.exists = True

            return True
    

    def delete(self):
        if not self.exists:
            return False
        
        db= app().make('db')
        connection = db.connection()

        ph = connection.placeholder
        sql = f"DELETE FROM {self.table} WHERE {self.primary_key} = {ph}"
        connection.execute(sql, [self.attributes[self.primary_key]])
        self.exists = False

        return True
    
    def to_dict(self):
        return {
            k:self.cast_attribute(k,v)
            for k,v in self.attributes.items()
        }

    def belongs_to(self, related, foreign_key=None, owner_key="id"):
        foreign_key = foreign_key or f"{related.__name__.lower()}_id"
        return BelongsTo(self, related, foreign_key, owner_key)
    
    def has_many(self, related, foreign_key=None, local_key='id'):
        foreign_key = foreign_key or f"{self.__class__.__name__.lower()}_id"
        return HasMany(self, related, foreign_key, local_key).get()
    
    def has_one(self, related, foreign_key=None, local_key='id'):
        foreign_key = foreign_key or f"{self.__class__.__name__.lower()}_id"
        return HasOne(self, related, foreign_key, local_key).get()
    
    def belongs_to_many(self,related,table=None,foreign_key=None,related_key=None,local_key='id',related_local_key='id'):
        name = related.__name__.lower()
        table = table or f"{self.table}_{name}s"
        foreign_key = foreign_key or f"{self.table[:-1]}_id"
        related_key = related_key or f"{name}_id"

        return BelognsToMany(self, related, table, foreign_key, related_key, local_key, related_local_key)
    
    def attach(self, ids):
        if not isinstance(ids, (list,tuple,set)):
            ids = [ids]
            db = app().make('db')
            conn = db.connection(self.parent.connection_name)