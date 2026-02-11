from core.orm.relations.relation import Relation

class HasMany(Relation):
    def __init__(self, parent, related, foreign_key, local_key):
        super().__init__(parent, related)
        self.foreign_key = foreign_key
        self.local_key = local_key

    def get(self):
        value = self.parent.attributes.get(self.local_key)
        return self.related.query().where(self.foreign_key, value).get()