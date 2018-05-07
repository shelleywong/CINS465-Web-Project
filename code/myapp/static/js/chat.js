//Reference: 2 (see: CINS465-Shelley-Wong, README.md)
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/chatroom/');

    chatSocket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var message = data['message'];
    document.querySelector('#chat-log').value += (data.username + ": " + message +
      " - " + data.created_on + ' UTC\n');

};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));

    messageInputDom.value = '';
};
