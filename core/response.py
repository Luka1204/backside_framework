import json

class Response:
    def __init__(self, body=None,status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {'Content-Type':'text/html'}

    @staticmethod
    def json(data, status=200, headers=None):
        headers = headers or {}
        headers.setdefault('Content-Type', 'application/json; charset=utf-8')
        body = json.dumps(data)
        return Response(body, status, headers)
    
    @staticmethod
    def text(data, status=200, headers=None):
        headers = headers or {}
        headers.setdefault('Content-Type', 'text/html; charset=utf-8')
        return Response(data, status, headers)
    @staticmethod
    def binary(data, status=200, headers=None):
        headers = headers or {}
        headers.setdefault('Content-Type', 'application/octet-stream')
        return Response(data, status, headers)
    
    def send(self):
        for k, v in self.headers.items():
            print(f"{k}: {v}")
        print(f'Status: {self.status}')
        print('\n'+str(self.body))