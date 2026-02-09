import os

_ENV = {}

def load_env(path='.env'):
    global _ENV

    if not os.path.exists(path):
        return
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line.strip()

            if not line or line.startswith('#'):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=",1)
            _ENV[key.strip()] = value.strip()

def env(key, default=None):
    return _ENV.get(key, default)