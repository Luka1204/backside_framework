class Middleware:
    def before(self, request):
        pass

    def after(self,request,response):
        return response