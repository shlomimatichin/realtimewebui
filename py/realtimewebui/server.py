from twisted.internet import reactor
from twisted.web import server
from autobahn.twisted.websocket import WebSocketServerFactory

from realtimewebui import modelwebsocketprotocol
from realtimewebui import render
from realtimewebui import tojs
from realtimewebui import basicauthresource
import sys
import signal


def _exit(*args):
    reactor.stop()
    sys.exit()

signal.signal(signal.SIGTERM, _exit)
signal.signal(signal.SIGINT, _exit)


def _websocketFactory(webSocketPort):
    websocketFactory = WebSocketServerFactory("ws://localhost:%d" % webSocketPort, debug=False)
    modelwebsocketprotocol.ModelWebSocketProtocol.model = tojs.model
    websocketFactory.protocol = modelwebsocketprotocol.ModelWebSocketProtocol
    reactor.listenTCP(webSocketPort, websocketFactory)


def runSecured(root, port, webSocketPort, username, password):
    render.DEFAULTS['globalModelWebsocketPort'] = webSocketPort
    securedRoot = basicauthresource.BasicAuthResource(root, username, password)
    reactor.listenTCP(port, server.Site(securedRoot))
    _websocketFactory(webSocketPort)
    reactor.run()


def runUnsecured(root, port, webSocketPort):
    render.DEFAULTS['globalModelWebsocketPort'] = webSocketPort
    reactor.listenTCP(port, server.Site(root))
    _websocketFactory(webSocketPort)
    reactor.run()
