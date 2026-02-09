from database.connection import Connection

class QueryBuilder:
    def __init__(self, connection, table):
        self.connection = connection
        self.table = table
        self.wheres=[]
        self.bindings = []
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
        cursor = self.connection.execute(self.to_sql(), self.bindings)
        return [dict(row) for row in cursor.fetchall()]
    
    def first(self):
        results = self.get()
        return results[0] if results else None