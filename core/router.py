class RouteDefinition:
    def __init__(self, method, uri, action):
        self.method = method
        self.uri = uri
        self.action = action
        self.name_alias = None
        self.middlewares = []

    def name(self, name):
        self.name_alias = name
        return self
    def middleware(self, *middlewares):
        self.middlewares.extend(middlewares)
        return self

    
    """ def match(self, request_path):
        route_parts = self.path.strip('/').split('/')
        request_parts = request_path.strip('/').split('/')
        if len(route_parts) != len(request_parts):
            return None
        params = {}
        for rp, rq in zip(route_parts, request_parts):
            if rp.startswith('{') and rp.endswith('}'):
                param_name = rp[1:-1]
                params[param_name] = rq
            elif rp != rq:
                return None
        return params """

class Router:
    def __init__(self, container=None):
        self.routes = []
        self.container = container
        self.middleware_aliases = {}
        self.middleware_groups = {}
        self._group_stack=[] #Stack para manejar grupos de rutas

    def alias_middleware(self, alias, middleware_cls):
        self.middleware_aliases[alias] = middleware_cls
    
    def middleware_group(self, name, middlewares):
        self.middleware_groups[name] = middlewares

    def get(self, uri, action):
        return self._add('GET',uri,action)
    def post(self, uri, action):
        return self._add('POST',uri,action)
    def put(self, uri, action):
        return self._add('PUT',uri,action)
    
    def patch(self, uri, action):
        return self._add('PATCH',uri,action)
    def delete(self, uri, action):
        return self._add('DELETE',uri,action)

    def group(self, *,prefix='', middleware=None, routes=None):
        middleware = middleware or []
        
        group = {
            'prefix':prefix,
            'middleware':middleware
        }

        self._group_stack.append(group)

        if callable(routes):
            routes(self)
        self._group_stack.pop()

    def _add(self, method, uri, action):
        full_uri = self._apply_prefix(uri)
        route = RouteDefinition(method, full_uri,action)

        for group in self._group_stack:
            route.middlewares.extend(group['middleware'])

        self.routes.append(route)
        return route
    
    def _apply_prefix(self, uri):
        prefixes=[g['prefix'] for g in self._group_stack if g['prefix']]
        full = '/'.join(p.strip('/') for p in prefixes + [uri])
        return '/' + full.strip('/')
    
    def resolve(self, request):
        for route in self.routes:
            if route.method != request.method:
                continue
            params = self._match(route.uri, request.path)
            if params is not None:
                request.params = params
                request.route = route
                return route
            return None
    
    def dispatch(self, request):
        route = self.resolve(request)
        if not route:
            raise Exception('Route not found')
        
        resolved_middlewares = []
        for mw in route.middlewares:
            if mw in self.middleware_groups:
                resolved_middlewares.extend(self.middleware_groups[mw])
            else:
                resolved_middlewares.append(mw)
        
        for mw in resolved_middlewares:
            mw_cls = self.middleware_aliases.get(mw)
            if mw_cls:
                mw_instance = self.container.resolve(mw_cls) if self.container else mw_cls()
                mw_instance.before(request)

        if isinstance(route.action, str):
            controller_name, method = route.action.split('@')
            controller_cls = self.container.resolve(controller_name)
            controller = controller_cls(request)
            response = getattr(controller,method)()
        else:
            response = route.action(request)

        for mw in reversed(resolved_middlewares):
            mw_cls = self.middleware_aliases.get(mw)
            if mw_cls:
                """ mw_instance = self.container.resolve(mw_cls) if self.container else mw_cls()
                response = mw_instance.after(request,response) """
                response = mw_cls.after(request,response)
        return response(self, request)
        route = self.resolve(request)
        if not route:
            raise Exception('Route not found')


        # Execute action
        if isinstance(route.action, str):
            controller_name, method = route.action.split('@')
            controller_cls = self.container.resolve(controller_name)
            controller = controller_cls(request)
            return getattr(controller, method)()
        else:
            return route.action(request)