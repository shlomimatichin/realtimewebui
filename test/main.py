from realtimewebui import server
from realtimewebui import rootresource
from realtimewebui import render
from realtimewebui import callbacks
from realtimewebui import tojs


def changeYuvu(** kwargs):
    tojs.set("yuvu", {'name': 'pash'})


render.addTemplateDir(".")
tojs.set("yuvu", {'name': 'yuvu'})
callbacks.callbacks["changeYuvu"] = changeYuvu
root = rootresource.rootResource()
server.runUnsecured(root, 2000, 2001)
