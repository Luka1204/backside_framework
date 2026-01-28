class Response:
    def __init__(self, content='',status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {'Content-Type':'text/html'}