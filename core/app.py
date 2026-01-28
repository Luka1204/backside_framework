from core.response import Response
class Application:
    def __init__(self):
        self.router = None
        self.container = None
        self.middlewares = []

    def set_router(self,router):
        self.router = router
    
    def set_container(self,container):
        self.container = container

    def add_middleware(self,middleware):
        self.middlewares.append(middleware)
    

    def handle(self,request):
        route=self.router.resolve(request)
        if not route:
            return Response('404 not found',404)
        
        all_middlewares = self.middlewares + route.middlewares

        for mw in all_middlewares:
            mw.before(request)
        
        response = route.handler(request)

        for mw in reversed(all_middlewares):
            response = mw.after(request,response)
        return response