from core.helpers.helpers import app
class BelognsToMany:
    def __init__(self, parent, related, table, foreign_key, related_key, local_key, related_local_key):
        self.parent = parent
        self.related = related
        self.table = table
        self.foreign_key = foreign_key
        self.related_key = related_key
        self.local_key = local_key
        self.related_local_key = related_local_key

    
    def get(self):
        qb = self.related.query()

        qb.join(self.table, f"{self.table}.{self.related_key}", '=',f"{self.related.table}.{self.related_local_key}")

        qb.where(
            f"{self.table}.{self.foreign_key}",self.parent.attributes[self.local_key]
        )

        return qb.get()
    
    def attach(self, ids):
        if not isinstance(ids, (list,tuple,set)):
            ids = [ids]
        db = app().make('db')
        conn = db.connection(self.parent.connection_name)

        ph = conn.placeholder

        for id in ids:
            sql = (
                f"INSERT INTO {self.table} "
                f"({self.foreign_key}, {self.related_key}) "
                f"VALUES ({ph}, {ph})"
                )
            conn.execute(sql,[self.parent.attributes[self.local_key], id])

    def detach(self, ids=None):
        db = app.make('make')
        conn = db.connection(self.parent.connection_name)

        ph = conn.placeholder

        sql = f"DELETE FROM {self.table} WHERE {self.foreign_key} = {ph}"
        bindings = [self.parent.attributes[self.local_key]]

        if ids:
            if not isinstance(ids, (list, tuple, set)):
                ids = [ids]

            placeholders = ', '.join([ph] * len(ids))
            sql += f" AND {self.related_key} IN ({placeholders})"
            bindings.extend(ids)
        conn.execute(sql, bindings)

