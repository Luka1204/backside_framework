class Container:
    def __init__(self):
        self.bindings = {}
        self.singletons = {}

    def bind(self, key, resolver):
        self.bindings[key] = resolver

    def singleton (self,key,resolver):
        self.singletons[key]=resolver

    def resolve(self, key):
        if key in self.singletons:
            if callable(self.singletons[key]):
                self.singletons[key] = self.singletons[key]()
            return self.singletons[key]
        return self.bindings[key]()