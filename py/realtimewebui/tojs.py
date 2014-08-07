from realtimewebui.model import Model

model = Model()
set = model.set
get = model.get


def appendAndCycle(objectID, value, maximumSize):
    global model
    current = model.get(objectID)
    if current is None:
        current = []
    assert isinstance(current, list)
    current.append(value)
    current = current[- maximumSize:]
    model.set(objectID, current)


def subset(objectID, key, value):
    global model
    all = model.get(objectID)
    if all is None:
        all = dict()
    all[key] = value
    model.set(objectID, all)


def subunset(objectID, key):
    global model
    all = model.get(objectID)
    if all is None:
        all = dict()
    if key in all:
        del all[key]
    model.set(objectID, all)


def subsetDefault(objectID, key, value):
    global model
    all = model.get(objectID)
    if all is None:
        all = dict()
    if key in all:
        return
    all[key] = value
    model.set(objectID, all)


def increment(objectID):
    global model
    value = model.get(objectID)
    if value is None:
        value = 0
    value += 1
    model.set(objectID, value)
