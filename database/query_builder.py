from database.connection import Connection

class QueryBuilder:
    def __init__(self, connection, table,model=None):
        self.connection = connection
        self.table = table
        self.model = model
        self.wheres=[]
        self.bindings = []
        self._with = []
    
    def __getattr__(self, name):
        scope=f"scope_{name}"
        if hasattr(self.model, scope):
            def wrapper(*args, **kwargs):
                getattr(self.model, scope)(self, *args, **kwargs)
                return self
            return wrapper
        raise AttributeError

    def with_(self, *relations):
        for rel in relations:
            self._with.append(rel.split('.'))
        return self
    def where(self,column,operator,value):
        if value is None:
            value = operator
            operator = '='
        self.wheres.append(f"{column} {operator} %s")
        self.bindings.append(value)
        return self

    def to_sql(self):
        sql = f"SELECT * FROM {self.table}"
        if self.wheres:
            sql += " WHERE " + " AND ".join(self.wheres)
        return sql
    
    def get(self):
        sql = self.to_sql()
        cursor = self.connection.execute(sql, self.bindings)
        rows = cursor.fetchall()

        if not self.model:
            return rows
        
        models = [self.model.hydrate(dict(row)) for row in rows]

        if self._with:
            self._eager_load(models, self._with)
        return models
    
    def _eager_load(self, models,relations, parent_model=None):
        for path in relations:
            self._load_relation_path(models,path)
    
    def _load_relation_path(self, models, path):
        if not models or not path:
            return
        relation_name = path[0]
        rel = getattr(self.models[0], relation_name)

        if not hasattr(rel, 'foreign_key'):
            return
        
        ids = [m.attributes[m.primary_key] for m in models]

        results = rel.related.query().where_in(rel.foreign_key, ids).get()

        grouped = {}

        for r in results:
            grouped.setdefault(r.attributes[rel.foreign_key],[]).append(r)

        for m in models:
            m.attributes[relation_name] = grouped.get(m.attributes[m.primary_key],[])

    def where_in(self, column, values):
        if not values:
            self.wheres.append("1 = 0")
            return self
        
        ph = self.connection.placeholder
        placeholders = ', '.join([ph] * len(values))

        self.wheres.append(f"{column} IN ({placeholders})")
        self.bondings.extend(values)

        return self
    
    def first(self):
        results = self.get()
        return results[0] if results else None