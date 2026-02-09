from core.orm.model import Model

class User(Model):
    table = "users"
    fillable = ["nombre"]