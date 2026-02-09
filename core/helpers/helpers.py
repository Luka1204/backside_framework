_app = None

def set_app(app):
    global _app
    _app = app

def app():
    return _app