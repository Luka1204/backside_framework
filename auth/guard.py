class Auth:
    user = None
    
    @classmethod
    def check(cls):
        return cls.user is not None
    
    @classmethod
    def login(cls, user):
        cls.user = user
    
    @classmethod
    def logout(cls):
        cls.user = None