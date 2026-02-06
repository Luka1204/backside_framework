from core.response import Response
class Kernel:
    def __init__(self, app):
        self.app = app
    
    def handle(self, request):
        router = self.app.make('router')
        route = router.match(request)
        if not route:
            return Response.text('404 Not Found', 404)

        middlewares = []
        for mw in route.middlewares:
            if mw in router.middleware_groups:
                middlewares += router.middleware_groups[mw]
            else:
                middlewares.append(mw)
        
        for mw in middlewares:
            router.middleware_aliases[mw]().before(request)
        
        if isinstance(route.action, str):
            ctrl, method = route.action.split('@')
            controller = self.app.make(ctrl)
            result = getattr(controller,method)(request)
        else:
            result = route.action(request)
        
        for mw in reversed(middlewares):
            result = router.middleware_aliases[mw]().after(request,result)
        
        return self.normalize_response(result)

    def normalize_response(self,result):
        if isinstance(result, Response):
            return result
        elif isinstance(result, (dict,list)):
            return Response.json(result)
        elif isinstance(result, bytes):
            return Response.binary(result)
        else:
            return Response.text(str(result))