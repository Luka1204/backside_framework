class Route:
    def __init__(self, method, path, handler, middleware=None):
        self.method = method
        self.path = path
        self.handler = handler
        self.middleware = middleware or []

class Router:
    def __init__(self):
        self.routes = {}

    def add(self,method,path,handler):
        self.routes[(method,path)] = handler
    
    def resolve(self,request):
        return self.routes.get((request.method, request.path))