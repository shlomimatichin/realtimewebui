from twisted.internet import reactor
import simplejson


class Model:
    def __init__(self):
        self._objects = dict()

    def set(self, objectID, value):
        reactor.callInThread(self._set, objectID, value)

    def get(self, objectID):
        self._emplace(objectID)
        return self._objects[objectID].getValue()

    def register(self, objectID, handler):
        self._emplace(objectID)
        self._objects[objectID].register(handler)

    def unregister(self, objectID, handler):
        self._objects[objectID].unregister(handler)

    def storeJSONFile(self, path):
        obj = {k: v.getValue() for (k, v) in self._objects.iteritems()}
        with open(path, "w") as f:
            simplejson.dump(obj, f, indent=2)

    def loadJSONFile(self, path):
        with open(path) as f:
            data = simplejson.load(f)
        for key, value in data.iteritems():
            self.set(key, value)

    def _emplace(self, objectID):
        if objectID not in self._objects:
            self._objects[objectID] = _Object(objectID)

    def _set(self, objectID, value):
        self._emplace(objectID)
        self._objects[objectID].setValue(value)


class _Object:
    def __init__(self, objectID):
        self.objectID = objectID
        self._value = None
        self.registered = []

    def register(self, handler):
        assert handler not in self.registered
        self.registered.append(handler)

    def unregister(self, handler):
        assert handler in self.registered
        self.registered.remove(handler)

    def setValue(self, value):
        self._value = value
        for registered in list(self.registered):
            registered.updateObject(self.objectID)

    def getValue(self):
        return self._value
