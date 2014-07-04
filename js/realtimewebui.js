function RealTimeWebUI()
{
    var self = this;
    self._canSend = false;
    self._registered = new Object;

    self.register = function(objectID, callback) {
        if (self._registered[objectID] === undefined) {
            self._registered[objectID] = [callback];
            self._sendRegisterMessage(objectID);
        } else {
            self._registered[objectID].push(callback);
        }
    };

    self.command = function(command, parameters) {
        var data = {cmd: command, parameters: parameters};
        self._websocket.send(JSON.stringify(data))
    };

    self._sendRegisterMessage = function(objectID) {
        if (! self._canSend)
            return;
        var data = {objectID: objectID, cmd: '__register__'};
        self._websocket.send(JSON.stringify(data))
    }

    self._connect = function() {
        var parts = window.location.href.split("/");
        var hostname = parts[2].split(":")[0];
        self._websocket = new WebSocket("ws://" + hostname + ":" + globalModelWebsocketPort);
        self._websocket.onopen = self._onOpen;
        self._websocket.onmessage = self._onMessage;
        self._websocket.onerror = self._onError;
        self._websocket.onclose = self._onClose;
    };

    self._onOpen = function(event) {
        self._canSend = true;
        var authMessage = {cmd: '__auth__', secret: globalModelWebsocketSecret};
        self._websocket.send(JSON.stringify(authMessage));
        for (var objectID in self._registered)
            self._sendRegisterMessage(objectID);
    };

    self._onMessage = function(event) {
        var data = JSON.parse(event.data);
        if (data.type != 'updateObjects') {
            console.error('unknown event from server: ' + data);
            return;
        }
        for (var objectID in data.objects) {
            var value = data.objects[objectID];
            self._handleUpdateObject(objectID, value);
        }
    };

    self._handleUpdateObject = function(objectID, value) {
        for (var i in self._registered[objectID]) {
            var callback = self._registered[objectID][i];
            callback(value);
        }
    };

    self._onError = function(event) {
        console.error("Error in websocket: " + event);
        self._canSend = false;
        self._retryConnect();
    };

    self._onClose = function(event) {
        console.error("Websocket closed");
        self._canSend = false;
        self._retryConnect();
    };

    self._retryConnect = function() {
        setTimeout(self._connect, 1000);
    };

    $(function() {self._connect();});
}
