from core.response import Response
from core.container import Container
from core.http.kernel import Kernel
class Application(Container):
    def __init__(self):
        super().__init__()
        self.router = None
        self.container = None
        self.middlewares = []
        self.providers = []
        self.singleton('kernel',lambda:Kernel(self))


    def set_router(self, router):
        self.router = router


    def set_container(self, container):
        self.container = container


    def add_middleware(self, middleware):
        self.middlewares.append(middleware)


    def register_provider(self, provider_cls):
        provider = provider_cls(self)
        provider.register()
        self.providers.append(provider)


    def boot(self):
        for provider in self.providers:
            provider.boot()


    def run(self, method="GET", path="/", headers=None, body=None, query=None):
        from core.request import Request
        request = Request(method, path, headers, body, query)
        kernel = self.make('kernel')
        response = kernel.handle(request)
        response.send()
        return response
    """ def handle(self, request):
        route = self.router.resolve(request)
        if not route:
            return Response('404 Not Found', 404)


        all_middlewares = self.middlewares + route.middlewares


        for mw in all_middlewares:
            mw.before(request)


        response = route.handler(request)


        for mw in reversed(all_middlewares):
            response = mw.after(request, response)


        return response """