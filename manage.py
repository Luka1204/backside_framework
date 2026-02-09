from bootstrap.app import create_app
from core.http.kernel import Kernel
from core.request import Request

app = create_app()
kernel = Kernel(app)

""" db = app.make('db')
conn = db.connection()

rows = conn.select("SELECT 1 AS test") """

response = kernel.handle(Request("GET",'/'))
response.send()