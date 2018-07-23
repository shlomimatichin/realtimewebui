from twisted.web import resource
from twisted.web import static
from realtimewebui import config
from realtimewebui import render


GLOBAL_PARAMETERS = dict()


def rootResource():
    return RootResource()


class Renderer(resource.Resource):
    def __init__(self, templateName, parameters):
        resource.Resource.__init__(self)
        self._templateName = templateName
        self._parameters = dict(GLOBAL_PARAMETERS)
        self._parameters.update(parameters)

    def render(self, request):
        return render.render(self._templateName, self._parameters)


class RootResource(resource.Resource):
    def getChildWithDefault(self, path, request):
        path = path.decode()
        if path == "realtimewebui":
            return static.File(config.REALTIMEWEBUI_ROOT_DIRECTORY)
        if path == '':
            return Renderer("index.html", {})
        return Renderer(path, {})
