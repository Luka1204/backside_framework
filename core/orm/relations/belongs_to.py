from core.orm.relations.relation import Relation

class BelongsTo(Relation):
    def __init__(self, parent, related, foreign_key, owner_key):
        super().__init__(parent, related)
        self.foreign_key = foreign_key
        self.owner_key = owner_key

    def get(self):
        key = self.parent.attributes.get(self.foreign_key)
        if key is None:
            return None
        
        parent = self.related.query().where(self.woner_key,key).first()

        if parent:
            parent.attributes[self.parent.__class__.__name__.lower()] = self.parent
        
        return parent