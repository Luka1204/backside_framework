class Request:
    def __init__(self, method, path, headers=None, body=None, query=None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body
        self.query = query or {}
        self.params = {}

    def input(self, key, default=None):
        if key in self.body:
            return self.body[key]
        if key in self.query:
            return self.query[key]
        return default