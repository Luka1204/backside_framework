from http.controllers.home_controller import HomeController

def register_routes(router):
    router.add_route('GET', '/', lambda req:HomeController(req).index())