from service_provider import ServiceProvider
class RouteServiceProvider(ServiceProvider):
    def boot(self):
        from routes.web import register_routes
        register_routes(self.app.router)