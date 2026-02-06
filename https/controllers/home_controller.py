from core.response import Response
from core.http.controller import Controller

class HomeController(Controller):
    def index(self,request):
        return {"response":'Bienvenido a Backside Framework!',"Status":200}