class Controller:
    def __init__(self, request=None):
        self.request = request
    
    def middleware(self):
        return []