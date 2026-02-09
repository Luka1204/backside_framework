import json

class Response:
    def __init__(self, body=None,status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {'Content-Type':'text/html'}

    def __str__(self):
        if self.body is None:
            return ''
        
        if isinstance(self.body, (bytes,bytearray)):
            return self.body.decode(errors='ignore')
        
        if (isinstance(self.body, (dict, list))):
            return json.dumps(self.body, ensure_ascii=False)
        
        return str(self.body)
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