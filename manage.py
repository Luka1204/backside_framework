from core.app import Application
from core.router import Router
from core.request import Request
from core.container import Container
from core.providers.route_service_provider import RouteServiceProvider


app = Application()
router = Router()
container = Container()


app.set_router(router)
app.set_container(container)


# Register Providers (Laravel-style)
app.register_provider(RouteServiceProvider)
app.boot()


request = Request('GET', '/')
response = app.handle(request)
print(response.content)


from core.app import Application
from core.router import Router
from core.request import Request
from core.container import Container
from database.connection import Database
from orm.model import Model
from http.controllers.home_controller import home


app = Application()
router = Router()
container = Container()


db = Database()
Model.set_database(db)


router.add('GET', '/', home)


app.set_router(router)
app.set_container(container)


request = Request('GET', '/')
response = app.handle(request)
print(response.content)