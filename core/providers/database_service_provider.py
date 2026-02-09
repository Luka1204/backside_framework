from database.database_manager import DatabaseManager
class DatabaseServiceProvider:
    def __init__(self, app):
        self.app=app
        
    def register(self):
        def resolver():
            config = self.app.make("config").get("database")
            return DatabaseManager(config)
        self.app.singleton("db",resolver)
    
    def boot(self):
        pass