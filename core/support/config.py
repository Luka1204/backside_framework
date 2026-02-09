import importlib

class ConfigRepository:
    def __init__(self):
        self.items={}

    def load(self, name):
        module = importlib.import_module(f"config.{name}")
        self.items[name] = module.config()

    def get(self, key, default=None):
        parts = key.split(".")
        value = self.items

        for part in parts:
            if part not in value:
                return default
            value = value[part]
        
        return value