import os
import importlib
import inspect

from core.http.controller import Controller

class ControllerServiceProvider:
    def __init__(self, app):
        self.app = app
    
    def register(self):
        controllers_path="app/https/controllers"

        for root,_,files in os.walk(controllers_path):
            for file in files:
                if not file.endswith("_controller.py"):
                    continue
                module_path = self._module_path(root, file)
                module = importlib.import_module(module_path)

                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if self._is_controller(obj):
                        self._bind_controller(obj)
    def boot(self):
        pass

    def _module_path(self, root, file):
        path = os.path.join(root,file)
        path = path.replace("\\",".").replace("/",".")
        path = path.replace(".py","")
        return path
    

    def _is_controller(self, cls):
        return (
            issubclass(cls, Controller)
            and cls is not Controller
            and cls.__name__.endswith("Controller")
        )
    
    def _bind_controller(self, controller_class):
        name = controller_class.__name__
        self.app.bind(name, lambda cls=controller_class: cls())