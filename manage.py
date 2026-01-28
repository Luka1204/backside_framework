from core.app import Application
from core.router import Router
from core.request import Request
from core.container import Container
from database.connection import Database
from orm.model import Model

app = Application()
router = Router()
container = Container()

db = Database()
Model.set_database(db)

router.add('GET','/',lambda req: app.handle_request(req))

app.set_router(router)
app.set_container(container)

request = Request('GET','/')
response = app.handle(request)
print(response.content)