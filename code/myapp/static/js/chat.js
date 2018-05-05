
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

// $(function() {
//     // When we're using HTTPS, use WSS too.
//     var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
//     var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
//
//     chatsock.onmessage = function(message) {
//         var data = JSON.parse(message.data);
//         var chat = $("#chat")
//         var ele = $('<tr></tr>')
//
//         ele.append(
//             $("<td></td>").text(data.created_on)
//         )
//         ele.append(
//             $("<td></td>").text(data.message)
//         )
//         ele.append(
//             $("<td></td>").text(data.message_html)
//         )
//
//         chat.append(ele)
//     };
//
//     $("#chatform").on("submit", function(event) {
//         var message = {
//             message: $('#message').val(),
//             message_html: $('#message_html').val(),
//         }
//         chatsock.send(JSON.stringify(message));
//         $("#message").val('').focus();
//         return false;
//     });
// });
