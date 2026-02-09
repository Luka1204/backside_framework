from core.support.env import env
from core.providers.route_service_provider import RouteServiceProvider
from core.providers.database_service_provider import DatabaseServiceProvider
from core.providers.controller_service_provider import ControllerServiceProvider
def config():
    return {
        "name":"Backside Framework",
        "env":env("APP_ENV","production"),
        "debug":env("APP_DEBUG",False) == "true",
        "providers":[
            RouteServiceProvider,
            DatabaseServiceProvider,
            ControllerServiceProvider
        ]
    }