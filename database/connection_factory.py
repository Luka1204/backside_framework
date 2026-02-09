from database.drivers.sqlite import SQLiteConnection
from database.drivers.mysql import MySQLConnection

class ConnectionFactory:
    drivers = {
        'sqlite':SQLiteConnection,
        'mysql':MySQLConnection
    }

    @classmethod
    def make(cls, driver, config):
        if driver not in cls.drivers:
            raise Exception(f"Unsupported database driver: {driver}")
        
        return cls.drivers[driver](config)