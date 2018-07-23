import os
import jinja2
from realtimewebui import config

DEFAULTS = dict(title="UI", brand="UI")
_htmlDir = os.path.join(config.REALTIMEWEBUI_ROOT_DIRECTORY, "html")
_templateDirs = [_htmlDir]
_loader = None
_env = None


def addTemplateDir(dir):
    global _templateDirs
    global _loader
    global _env
    _templateDirs.append(dir)
    _loader = jinja2.FileSystemLoader(_templateDirs)
    _env = jinja2.Environment(loader=_loader)


def render(template, parameters):
    global _env

    withDefaults = dict(DEFAULTS)
    withDefaults.update(parameters)
    content = _env.get_template(template).render(**withDefaults)
    return content.encode('utf-8')


def renderToFile(output, template, parameters):
    content = render(template, parameters)
    with open(output, "wb") as f:
        f.write(content)


if __name__ == "__main__":
    import sys
    print(render(sys.argv[1], {}))
