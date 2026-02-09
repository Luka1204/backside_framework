from core.support.env import env

def config():
    return {
        "default" : env("DB_CONNECTION",'mysql'),
        "connections":{
            "mysql":{
                "driver":"mysql",
                "database":env("DB_DATABASE","database/app.db")
            }
        }
    }