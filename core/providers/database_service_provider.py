from database.database_manager import DatabaseManager
class DatabaseServiceProvider:
    def __init__(self, app):
        self.app=app
        
    def register(self):
        config = self.app.make('config').get('database')
        self.app.singleton("db",lambda:DatabaseManager(config))
    
    def boot(self):
        pass