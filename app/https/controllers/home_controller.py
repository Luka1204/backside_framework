from core.response import Response
from core.http.controller import Controller
from app.models.user import User

class HomeController(Controller):
    def index(self,request):
        user = User()
        user.nombre = "Luka"
        user.save()
        print(user.id)
        id = int(user.id)
        
        print(user.find(1))

        return {"response":'Bienvenido a Backside Framework!',"Status":200}
    
    def admin(self, request):
        return {"response":'Bienvenido a Admin Backside Framework!',"Status":200}