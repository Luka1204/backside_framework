from core.response import Response
from core.http.controller import Controller

class HomeController(Controller):
    def index(self):
        return Response('Bienvenido a Backside Framework!')