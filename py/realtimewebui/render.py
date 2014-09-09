import os
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = __name__
SECRET_KEY = "ABAB"
from realtimewebui import config
_htmlDir = os.path.join(config.REALTIMEWEBUI_ROOT_DIRECTORY, "html")
TEMPLATE_DIRS = [_htmlDir]
import django.template.loader


DEFAULTS = dict(title="UI", brand="UI")


def addTemplateDir(dir):
    TEMPLATE_DIRS.append(dir)


def render(template, parameters):
    withDefaults = dict(DEFAULTS)
    withDefaults.update(parameters)
    content = django.template.loader.render_to_string(template, withDefaults)
    return content.encode('utf-8')


def renderToFile(output, template, parameters):
    content = render(template, parameters)
    with open(output, "wb") as f:
        f.write(content)


if __name__ == "__main__":
    import sys
    print render(sys.argv[1], {})
