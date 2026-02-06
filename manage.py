from core.app import Application
from core.providers.route_service_provider import RouteServiceProvider
from https.controllers.home_controller import HomeController

app = Application()

# Controllers binding
app.bind('HomeController', lambda: HomeController())

# Providers
app.register_provider(RouteServiceProvider)
app.boot()

# Run application (Application controla todo)
app.run('GET' ,'/admin')
app.run('GET' ,'/')