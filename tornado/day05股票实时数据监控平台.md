## 股票实时监控平台

##### 服务器端：tornado websocket


```python
# 实时数据websocket
class DataRefreshHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        print('open')
        self.write_message(json.dumps(get_data(10)).encode())

        # 开启线程每隔3秒发送一次数据
        # Tornado5开始使用线程必须指定事件循环的策略否则无法启动线程
        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
        threading.Thread(target=send_data, args=(self,)).start()

```
生成模拟股票数据

```python
# 创建数据
def get_data(num):
    current_time = datetime.now()
    base_ss_value = 2500

    data = []
    for _ in range(num):
        current_ss_value = base_ss_value + random.randint(-1000, 1000)
        current_time_str = "%d-%d-%d" % (current_time.year, current_time.month, current_time.day)
        data.append([current_time_str, current_ss_value])
        current_time += timedelta(days=1)
    print(data)
    return data
```

后端定时发送数据

```python
# 发送数据: 异步发送
def send_data(ws_client):
    while True:
        print('send_data')
        time.sleep(3)

        data = get_data(10)
        ws_client.write_message(json.dumps(data).encode())

```

前端数据可视化： 使用echats图表库

<https://www.echartsjs.com/examples/zh/index.html>

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h2>股票实时监控平台</h2>
    <hr>

    <div id="main" style="width: 600px; height: 400px;">
    </div>

    <script src="https://cdn.bootcss.com/echarts/4.2.1-rc1/echarts.min.js"></script>
    <script>
        // 初始化echarts
        let mychart = echarts.init(main);
        var data = [];

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '上证指数实时数据'
            },
            xAxis: {
                type: 'time',
            },
            yAxis: {
                type: 'value',
            },
            series: [{
                type: 'line',
              	animation: false,
                data: data
            }]
        };

        // 使用刚指定的配置项和数据显示图表
        mychart.setOption(option);

        var ws = new WebSocket('ws://127.0.0.1/data/');
        ws.onmessage = function (e) {
            // 得到服务器最新数据
            data = JSON.parse(e.data);
            // 刷新图表
            mychart.setOption({series: [{data: data}]})
        }
    </script>
</body>
</html>
```





