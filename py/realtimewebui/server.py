from twisted.cred.portal import Portal
from twisted.cred import checkers
from twisted.internet import reactor

from zope.interface import implements
from twisted.cred.portal import IRealm
from twisted.web.resource import IResource
from twisted.web.guard import HTTPAuthSessionWrapper, DigestCredentialFactory
from twisted.web import server
from autobahn.twisted.websocket import WebSocketServerFactory

from realtimewebui import modelwebsocketprotocol
from realtimewebui import render
from realtimewebui import tojs

import sys
import signal


def _exit(*args):
    reactor.stop()
    sys.exit()

signal.signal(signal.SIGTERM, _exit)
signal.signal(signal.SIGINT, _exit)


class _PublicHTMLRealm(object):
    implements(IRealm)

    def __init__(self, root):
        self._root = root

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IResource in interfaces:
            return (IResource, self._root, lambda: None)
        raise NotImplementedError()


def _websocketFactory(webSocketPort):
    websocketFactory = WebSocketServerFactory("ws://localhost:%d" % webSocketPort, debug=False)
    modelwebsocketprotocol.ModelWebSocketProtocol.model = tojs.model
    websocketFactory.protocol = modelwebsocketprotocol.ModelWebSocketProtocol
    reactor.listenTCP(webSocketPort, websocketFactory)


def runSecured(root, port, webSocketPort, username, password):
    render.DEFAULTS['globalModelWebsocketPort'] = webSocketPort
    checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(** {username: password})
    portal = Portal(_PublicHTMLRealm(root), [checker])
    credentialFactory = DigestCredentialFactory("md5", "localhost:8080")
    rootAuth = HTTPAuthSessionWrapper(portal, [credentialFactory])
    reactor.listenTCP(port, server.Site(rootAuth))
    _websocketFactory(webSocketPort)
    reactor.run()


def runUnsecured(root, port, webSocketPort):
    render.DEFAULTS['globalModelWebsocketPort'] = webSocketPort
    reactor.listenTCP(port, server.Site(root))
    _websocketFactory(webSocketPort)
    reactor.run()
