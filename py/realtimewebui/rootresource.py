from twisted.web import resource
from twisted.web import static
import realtimewebui
from realtimewebui import render
import os


def rootResource():
    projectRootDir = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(realtimewebui.__file__))))
    externalsDir = os.path.join(projectRootDir, "externals")
    jsDir = os.path.join(projectRootDir, "js")
    root = resource.Resource()
    root.putChild("externals", static.File(externalsDir))
    root.putChild("realtimewebui", static.File(jsDir))
    root.putChild("index", Renderer("index.html", {}))
    return root


class Renderer(resource.Resource):
    def __init__(self, templateName, parameters):
        resource.Resource.__init__(self)
        self._templateName = templateName
        self._parameters = parameters

    def render(self, request):
        return render.render(self._templateName, self._parameters)
