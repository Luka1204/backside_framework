from  https.controllers.home_controller import HomeController

def routes(router):
    router.get('/', 'HomeController@index').name('home')
    router.get('/admin', 'HomeController@admin').name('admin')