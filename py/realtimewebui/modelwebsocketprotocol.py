import simplejson
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol
from realtimewebui import render
from realtimewebui import callbacks
import random
import string


_secret = "".join(random.choice(string.letters) for x in xrange(128))
render.DEFAULTS['globalModelWebsocketSecret'] = _secret


class ModelWebSocketProtocol(WebSocketServerProtocol):
    model = None

    def onOpen(self):
        self.__authTimeout = None
        self.__registered = []
        self.__authTimeout = reactor.callLater(5, self.__timeout)

    def __cancelTimeout(self):
        if self.__authTimeout is None:
            return
        authTimeout = self.__authTimeout
        self.__authTimeout = None
        authTimeout.cancel()

    def onClose(self, wasClean, code, reason):
        self.__cancelTimeout()
        for registered in self.__registered:
            self.model.unregister(registered, self)

    def onMessage(self, message, isBinary):
        try:
            data = simplejson.loads(message)
            self.__handle(data)
        except:
            self.__cancelTimeout()
            self.dropConnection()
            raise

    def updateObject(self, objectID):
        data = dict(objects={objectID: self.model.get(objectID)}, type='updateObjects')
        self.sendMessage(simplejson.dumps(data), isBinary=False)

    def __timeout(self):
        self.__authTimeout = None
        self.dropConnection()

    def __handle(self, data):
        if data['cmd'] != '__auth__' and self.__authTimeout:
            self.dropConnection()
            return
        if data['cmd'] == '__auth__':
            if self.__authTimeout is None:
                self.dropConnection()
                return
            if data['secret'] != _secret:
                self.dropConnection()
                return
            self.__cancelTimeout()
        elif data['cmd'] == '__register__':
            assert data['objectID'] not in self.__registered
            self.model.register(data['objectID'], self)
            self.__registered.append(data['objectID'])
            self.updateObject(data['objectID'])
        elif data['cmd'] == '__unregister__':
            assert data['objectID'] in self.__registered
            self.__registered.remove(data['objectID'])
            self.model.unregister(data['objectID'], self)
        else:
            callback = callbacks.callbacks[data['cmd']]
            callback(** data['parameters'])
