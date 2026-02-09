from bootstrap.app import create_app
from core.http.kernel import Kernel
from core.request import Request

app = create_app()
kernel = Kernel(app)

response = kernel.handle(Request("GET",'/'))
response.send()