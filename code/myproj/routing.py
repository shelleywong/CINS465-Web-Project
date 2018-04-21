from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# Point the root routing configuration at the chat.routing module.
# When a connection is made to the Channels development server, ProtocolTypeRouter
# first inspects the type of connection. If a WebSocket connection, (ws:// or wss://),
# the connection will be given to the AuthMiddlewareStack, which will populate
# the connection’s scope with a reference to the currently authenticated user.
# Then URLRouter will examine the HTTP path of the connection to route it to a 
# particular consumer
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
