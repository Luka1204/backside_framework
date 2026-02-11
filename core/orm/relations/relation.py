class Relation:
    def __init__(self, parent, related):
        self.parent = parent
        self.related = related
    
    def get(self):
        raise NotImplementedError