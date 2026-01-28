class Request:
    def __init__(self, method, path, headers=None, body=None, query=None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body
        self.query = query or {}