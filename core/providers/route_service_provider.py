from service_provider import ServiceProvider
class RouteServiceProvider(ServiceProvider):
    def boot(self):
        form routes.web import load_routes
        load_routes(self.app.router)