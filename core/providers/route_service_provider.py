from core.providers.service_provider import ServiceProvider
from core.router import Router
class RouteServiceProvider(ServiceProvider):

    def register(self):
        self.app.singleton('router', lambda: Router(self.app))
    def boot(self):
        from routes.web import routes
        routes(self.app.make('router'))