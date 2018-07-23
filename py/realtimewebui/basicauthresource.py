from twisted.web import resource
import base64


class BasicAuthResource(resource.Resource):
    def __init__(self, wrap, username, password):
        self._wrap = wrap
        self._username = username
        self._password = password
        self._expectedAuth = \
            "Basic " + base64.b64encode(('%s:%s' % (username, password)).encode()).decode()
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        if not self._authenticated(request):
            return self
        return self._wrap.getChild(path, request)

    def getChildWithDefault(self, path, request):
        if not self._authenticated(request):
            return self
        return self._wrap.getChildWithDefault(path, request)

    def render(self, request):
        if not self._authenticated(request):
            return
        return self._wrap.render(request)

    def _authenticated(self, request):
        credentials = request.getHeader("Authorization")
        if credentials is None:
            self._replyNotAllowed(request)
            return False
        if not credentials.startswith(self._expectedAuth):
            self._replyNotAllowed(request)
            return False
        return True

    def _replyNotAllowed(self, request):
        request.setResponseCode(401, b"Not Allowed")
        request.setHeader('WWW-Authenticate', 'Basic realm="realtimewebui"')
        request.setHeader('Content-type', 'text/html')
        request.write(b"Not Allowed")
