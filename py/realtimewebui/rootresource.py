from twisted.web import resource
from twisted.web import static
from realtimewebui import config
from realtimewebui import render


GLOBAL_PARAMETERS = dict()


def rootResource():
    root = resource.Resource()
    root.putChild("realtimewebui", static.File(config.REALTIMEWEBUI_ROOT_DIRECTORY))
    root.putChild("", Renderer("index.html", {}))
    return root


class Renderer(resource.Resource):
    def __init__(self, templateName, parameters):
        resource.Resource.__init__(self)
        self._templateName = templateName
        self._parameters = dict(GLOBAL_PARAMETERS)
        self._parameters.update(parameters)

    def render(self, request):
        return render.render(self._templateName, self._parameters)
