from core.app import Application
from core.support.env import load_env
from core.support.config import ConfigRepository
from core.helpers.helpers import set_app

def create_app():
    load_env()

    app = Application()
    config = ConfigRepository()
    config.load("app")
    config.load("database")
    
    app.singleton("config", lambda:config)

    app_config = config.get("app")
    for provider in app_config["providers"]:
        app.register_provider(provider)

    app.boot()
    set_app(app)

    return app