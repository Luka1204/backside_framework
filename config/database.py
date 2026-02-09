from core.support.env import env

def config():
    return {
        "default" : env("DB_CONNECTION",'mysql'),
        "connections": {
            'mysql': {
                'driver': 'mysql',
                'host': '127.0.0.1',
                'port': 3306,
                'database': 'backside',
                'username': 'root',
                'password': '',
                'charset': 'utf8mb4'
            },

            'sqlite': {
                'driver': 'sqlite',
                'database': 'database.sqlite'
            }
        }
    }