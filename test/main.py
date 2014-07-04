from realtimewebui import server
from realtimewebui import model
from realtimewebui import rootresource
from realtimewebui import render
from realtimewebui import callbacks


def changeYuvu(** kwargs):
    global theModel
    theModel.set("yuvu", {'name': 'pash'})


render.addTemplateDir(".")
theModel = model.Model()
theModel.set("yuvu", {'name': 'yuvu'})
callbacks.callbacks["changeYuvu"] = changeYuvu
root = rootresource.rootResource()
server.runUnsecured(root, theModel, 2000, 2001)
