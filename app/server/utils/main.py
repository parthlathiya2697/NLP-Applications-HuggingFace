html1 = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket(`ws://91bd-2405-201-200c-9177-c912-8169-9f31-e55c.ngrok.io/ws/614acc2a1e7f82f5391d0eea/6149bf78ad10593161b2b8fa`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var obj = {
                    content: input.value
                }
                ws.send(JSON.stringify(obj))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

html_home = """
<!DOCTYPE html>
<html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>
            Welcome to Hugging AI
        </h1>
    </body>
</html>
"""