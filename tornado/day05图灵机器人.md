## 图灵聊天机器人

图灵机器人官网： <http://www.turingapi.com/>


```python
class RobotHandler(tornado.websocket.WebSocketHandler):
    user_list = []
    def open(self, *args, **kwargs):
        self.user_list.append(self)

    async def on_message(self, message):
        client = AsyncHTTPClient()
        data = {
                'perception': {
                    'inputText': {
                        'text': message,
                    }
                },
                'userInfo': {
                "apiKey": "f67b098e8eb74d4b969f6d7f6c33a349",
                "userId": "258595",
            }
        }

    res = await client.fetch(
        'http://openapi.tuling123.com/openapi/api/v2',
        method='POST',
        body = json.dumps(data).encode()
    )
    print(res.body.decode('utf-8'))
    res_dict = json.loads(res.body.decode('utf-8'))
    self.write_message(res_dict['results'][0]['values']['text'])

    def on_close(self):
        self.user_list.remove(self）
          
```
js

    <script>
        let ws = new WebSocket('ws://127.0.0.1:8888/robot/')
        ws.onmessage = function (evt) {
            console.log(evt.data)
            $('#result').append($('<p>').text('答：' +evt.data))
        }
    
        $('#send').click(function () {
            let msg = $('#content').val()
            if (msg.length > 0){
                ws.send(msg)
                $('#result').append('<P>问：' + msg + '<p>')
            }
        })
    </script>
