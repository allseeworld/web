## Day04 Tornado异步化

### 一. 预备知识

#### 并发编程  

```
同步 ：先执行前面的，然后再执行后面的代码，按顺序依次执行。
异步 ：后面的代码不需要等待前面代码执行完成后才执行。处理比较耗时的操作，可以使用异步：网络请求,数据库操作,文件操作。

并行：线程数量 <= CPU数量
并发：线程数量 > CPU数量
```

所谓并发编程就是让程序中有多个部分能够并发或同时执行，并发编程带来的好处不言而喻，其中最为关键的两点是提升了执行效率和改善了用户体验。下面简单阐述一下Python中实现并发编程的3种方式：

```
1.多线程：Python中通过`threading`模块的`Thread`类来支持多线程编程。Python解释器通过GIL（全局解释器锁）来防止多个线程同时执行本地字节码，这个锁对于CPython（Python解释器的官方实现）是必须的，因为CPython的内存管理并不是线程安全的。因为GIL的存在，Python的多线程并不能利用CPU的多核特性。
协程：线程中的，一个进程可以有多个线程， 一个线程可以有多个协程。不能使用多核。
 
2.多进程：使用多进程可以有效的解决GIL的问题，Python中的`multiprocessing`模块提供了`Process`类来实现多进程，由于进程间的内存是相互隔离的（操作系统对进程的保护），进程间通信（共享数据）必须使用管道、套接字等方式，这一点从编程的角度来讲是比较麻烦的，为此，Python的`multiprocessing`模块提供了一个名为`Queue`的类，它基于管道和锁机制提供了多个进程共享的队列。 

3.异步编程（异步I/O）：所谓异步编程是通过调度程序从任务队列中挑选任务，调度程序以交叉的形式执行这些任务，我们并不能保证任务将以某种顺序去执行，因为执行顺序取决于队列中的一项任务是否愿意将CPU处理时间让位给另一项任务。异步编程通常通过多任务协作处理的方式来实现，由于执行时间和顺序的不确定，因此需要通过callback（回调函数v6.0之后已取消）或者`Future`对象来获取任务执行的结果。目前我们使用的Python 3通过`asyncio`模块以及`await`和`async`关键字（Python 3.5中引入，Python 3.7中正式成为关键字）提供了对异步I/O的支持。
```

##### asyncio协程  

```Python
import asyncio

async def fetch(host):
    """从指定的站点抓取信息(协程函数)"""
    print(f'Start fetching {host}\n')
    # 跟服务器建立连接
    reader, writer = await asyncio.open_connection(host, 80)
    # 构造请求行和请求头
    writer.write(b'GET / HTTP/1.1\r\n')
    writer.write(f'Host: {host}\r\n'.encode())
    writer.write(b'\r\n')
    # 清空缓存区(发送请求)
    await writer.drain()
    # 接收服务器的响应(读取响应行和响应头)
    line = await reader.readline()
    while line != b'\r\n':
        print(line.decode().rstrip())
        line = await reader.readline()
    print('\n')
    writer.close()

def main():
    """主函数"""
    urls = ('www.sohu.com', 'www.douban.com', 'www.163.com')
    # 获取系统默认的事件循环
    loop = asyncio.get_event_loop()
    # 用生成式语法构造一个包含多个协程对象的列表
    tasks = [fetch(url) for url in urls]
    # 通过asyncio模块的wait函数将协程列表包装成Task（Future子类）并等待其执行完成
    # 通过事件循环的run_until_complete方法运行任务直到Future完成并返回它的结果
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    
if __name__ == 'main':
    main()
```
##### 三种方式的使用场景

   ```
我们对三种方式的使用场景做一个简单的总结。
以下情况需要使用多线程：
1. 程序需要维护许多共享的状态（尤其是可变状态），Python中的列表、字典、集合都是线程安全的，所以使用线程而不是进程维护共享状态的代价相对较小。
2. 程序会花费大量时间在I/O操作上，没有太多并行计算的需求且不需占用太多的内存。
	I/O操作: 网络请求,数据库操作,文件操作
	
以下情况需要使用多进程：
1. 程序执行计算密集型任务（如：字节码操作、数据处理、科学计算）。
2. 程序的输入可以并行的分成块，并且可以将运算结果合并。
3. 程序在内存使用方面没有任何限制且不强依赖于I/O操作（如：读写文件、套接字等）。

最后，如果程序不需要真正的并发性或并行性，而是更多的依赖于异步处理和回调时，异步I/O就是一种很好的选择。另一方面，当程序中有大量的等待与休眠时，也应该考虑使用异步I/O。

   ```
#### I/O模式和事件驱动

```
对于一次I/O操作（以读操作为例），数据会先被拷贝到操作系统内核的缓冲区中，然后从操作系统内核的缓冲区拷贝到应用程序的缓冲区（这种方式称为标准I/O或缓存I/O，大多数文件系统的默认I/O都是这种方式），最后交给进程。所以说，当一个读操作发生时（写操作与之类似），它会经历两个阶段：(1)等待数据准备就绪；(2)将数据从内核拷贝到进程中。
```

##### 由于存在这两个阶段，因此产生了以下几种I/O模式：

```
1.阻塞 I/O（blocking I/O）：进程发起读操作，如果内核数据尚未就绪，进程会阻塞等待 直到内核数据就绪并拷贝到进程的内存中。

2.非阻塞 I/O（non-blocking I/O）：进程发起读操作，如果内核数据尚未就绪，进程不阻塞而是收到内核返回的错误信息，进程收到错误信息可以再次发起读操作，一旦内核数据准备就绪，就立即将数据拷贝到了用户内存中，然后返回。

3.多路I/O复用（ I/O multiplexing）：监听多个I/O对象，当I/O对象有变化（数据就绪）的时候就通知用户进程。多路I/O复用的优势并不在于它单个I/O操作能处理得更快，而是在于能处理更多的I/O操作。

4.异步I/O（asynchronous I/O）：进程发起读操作后就可以去做别的事情了，内核收到异步读操作后会立即返回，所以用户进程不阻塞，当内核数据准备就绪时，内核发送一个信号给用户进程，告诉它读操作完成了。
```

##### 通常，我们编写一个处理用户请求的服务器程序时，有以下三种方式可供选择：

```
1.每收到一个请求，创建一个新的进程，来处理该请求；
2.每收到一个请求，创建一个新的线程，来处理该请求；
3.每收到一个请求，放入一个事件列表，让主进程通过非阻塞I/O方式来处理请求

第1种方式实现比较简单，但由于创建进程开销比较大，会导致服务器性能比较差；
第2种方式，由于要涉及到线程的同步，有可能会面临竞争、死锁等问题；
第3种方式，就是所谓事件驱动的方式，它利用了多路I/O复用和异步I/O的优点，虽然代码逻辑比前面两种都复杂，但能达到最好的性能，这也是目前大多数网络服务器采用的方式。

```

#### 同步异步，阻塞非阻塞的区别：

```python
同步, 异步: 客户端调用服务器接口时
阻塞, 非阻塞: 服务端发生等待

阻塞 -> 非阻塞
同步 -> 异步
性能优秀的系统一般是:异步非阻塞的方式（Tornado）web框架 + 高并发 + websocket(实时数据)
# Django姜戈 + Flask青花瓷 

异步非阻塞并不是消灭阻塞，而是将阻塞的任务放到不同的执行单元去执行 

```



## 二. Tornado异步化

```
在前面的例子中，我们并没有对`RequestHandler`中的`get`或`post`方法进行异步处理，这就意味着，一旦在`get`或`post`方法中出现了耗时间的操作，不仅仅是当前请求被阻塞，按照Tornado框架的工作模式，其他的请求也会被阻塞，所以我们需要对耗时间的操作进行异步化处理。
```

在Tornado稍早一些的版本中，可以用装饰器实现请求方法的异步化或协程化来解决这个问题。

```python
# 老的方法：使用@tornado.gen.coroutine + yield from
import tornado.web
import asyncio
import tornado.gen

class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        yield from asyncio.sleep(10)
        self.render('index.html')
        
# yield from使用参考文章: 
#	https://www.cnblogs.com/wongbingming/p/9085268.html

```

```Python
# 新的方法：使用asyncio的 async + await
import tornado.web
import asyncio

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        await asyncio.sleep(10)
        self.render('index.html')

```

##### 练习： 异步百度搜索

```python
# 异步百度搜索
class GetUrlHandler(tornado.web.RequestHandler):
    async def get(self):
        wd = self.get_argument('wd')
        client = AsyncHTTPClient()
        response = await client.fetch('http://www.baidu.com/s?wd=%s' %wd)
        self.write(response.body)
        
# 同步获取内容
class GetUrlHandler(tornado.web.RequestHandler):
    def get(self):
        wd = self.get_argument('wd')
        http_client = HTTPClient()
        response = http_client.fetch('http://www.baidu.com/s?wd=%s' %wd)
        self.write(response.body)

```



## 三. ab网站性能压力测试

```python
网站性能压力测试是服务器网站性能调优过程中必不可缺少的一环。只有让服务器处在高压情况下，才能真正体现出软件、硬件等各种设置不当所暴露出的问题。

性能测试工具目前最常见的有以下几种：ab、http_load、webbench、siege

ab是apache自带的压力测试工具。ab非常实用，它不仅可以对apache服务器进行网站访问压力测试，也可以对或其它类型的服务器进行压力测试。比如nginx、tomcat、IIS等。

一、ab的原理
ab是apache bench命令的缩写。

ab的原理：ab命令会创建多个并发访问线程，模拟多个访问者同时对某一URL地址进行访问。它的测试目标是基于URL的，因此，它既可以用来测试apache的负载压力，也可以测试nginx、lighthttp、tomcat、IIS等其它Web服务器的压力。

ab命令对发出负载的计算机要求很低，它既不会占用很高CPU，也不会占用很多内存。但却会给目标服务器造成巨大的负载，其原理类似CC攻击。自己测试使用也需要注意，否则一次上太多的负载。可能造成目标服务器资源耗完，严重时甚至导致死机。

二、ab的安装

三、ab参数说明
有关ab命令的使用，我们可以通过帮助命令进行查看： ab --help

参数说明：
-n 在测试会话中所执行的请求个数。默认时，仅执行一个请求。
-c 一次产生的请求个数。默认是一次一个。

-t 测试所进行的最大秒数。其内部隐含值是-n 50000，它可以使对服务器的测试限制在一个固定的总时间以内。默认时，没有时间限制。
-p 包含了需要POST的数据的文件。
-T POST数据所使用的Content-type头信息。
-v 设置显示信息的详细程度-4或更大值会显示头信息，3或更大值可以显示响应代码(404,200等),2或更大值可以显示警告和其他信息。
-V 显示版本号并退出。
-w 以HTML表的格式输出结果。默认时，它是白色背景的两列宽度的一张表。
-i 执行HEAD请求，而不是GET。
-x 设置<table>属性的字符串。
-X 对请求使用代理服务器。
-y 设置<tr>属性的字符串。
-z 设置<td>属性的字符串。
-C 对请求附加一个Cookie:行。其典型形式是name=value的一个参数对，此参数可以重复。
-H 对请求附加额外的头信息。此参数的典型形式是一个有效的头信息行，其中包含了以冒号分隔的字段和值的对(如,"Accept-Encoding:zip/zop;8bit")。
-A 对服务器提供BASIC认证信任。用户名和密码由一个:隔开，并以base64编码形式发送。无论服务器是否需要(即,是否发送了401认证需求代码)，此字符串都会被发送。
-h 显示使用方法。
-d 不显示"percentage served within XX [ms] table"的消息(为以前的版本提供支持)。
-e 产生一个以逗号分隔的(CSV)文件，其中包含了处理每个相应百分比的请求所需要(从1%到100%)的相应百分比的(以微妙为单位)时间。由于这种格式已经“二进制化”，所以比'gnuplot'格式更有用。
-g 把所有测试结果写入一个'gnuplot'或者TSV(以Tab分隔的)文件。此文件可以方便地导入到Gnuplot,IDL,Mathematica,Igor甚至Excel中。其中的第一行为标题。
-i 执行HEAD请求，而不是GET。
-k 启用HTTP KeepAlive功能，即在一个HTTP会话中执行多个请求。默认时，不启用KeepAlive功能。
-q 如果处理的请求数大于150，ab每处理大约10%或者100个请求时，会在stderr输出一个进度计数。此-q标记可以抑制这些信息。

四、ab性能指标
在进行性能测试过程中有几个指标比较重要：
1、吞吐率（Requests per second）rps
	服务器并发处理能力的量化描述，单位是reqs/s，指的是在某个并发用户数下单位时间内处理的请求数。某个并发用户数下单位时间内能处理的最大请求数，称之为最大吞吐率。
	记住：吞吐率是基于并发用户数的。这句话代表了两个含义：
		a、吞吐率和并发用户数相关
		b、不同的并发用户数下，吞吐率一般是不同的
		计算公式：总请求数/处理完成这些请求数所花费的时间，即
		这个数值表示当前机器的整体性能，值越大越好。

2、并发连接数（The number of concurrent connections）
	并发连接数指的是某个时刻服务器所接受的请求数目，简单的讲，就是一个会话。

3、并发用户数（Concurrency Level）
	要注意区分这个概念和并发连接数之间的区别，一个用户可能同时会产生多个会话，也即连接数。

4、用户平均请求等待时间（Time per request）
	计算公式：处理完成所有请求数所花费的时间/（总请求数/并发用户数）
	
5、服务器平均请求等待时间（Time per request:across all concurrent requests）
	计算公式：处理完成所有请求数所花费的时间/总请求数，即：

五、ab实际使用
	ab的命令参数比较多，我们经常使用的是-c和-n参数。
	示例：
		ab -c 10 -n 100 http://www.baidu.com/
	其中： 
		-c 10 表示并发用户数为10
		-n 100 表示请求总数为100
		http://www.baidu.com 表示请求的目标URL
	这行表示同时处理100个请求并运行10次index.php文件。

六、测试结果分析（*表示重要参数）
*Requests per second: apache测试出的吞吐率

Server Software表示被测试的Web服务器软件名称。
Server Hostname表示请求的URL主机名。
Server Port表示被测试的Web服务器软件的监听端口。
Document Path表示请求的URL中的根绝对路径，通过该文件的后缀名，我们一般可以了解该请求的类型。
Document Length表示HTTP响应数据的正文长度。

Concurrency Level表示并发用户数，这是我们设置的参数之一。
*Time taken for tests 表示所有这些请求被处理完成所花费的总时间。
Complete requests 表示总请求数量，这是我们设置的参数之一。
Failed requests 表示失败的请求数量，这里的失败是指请求在连接服务器、发送数据等环节发生异常，以及无响应后超时的情况。如果接收到的HTTP响应数据的头信息中含有2XX以外的状态码，则会在测试结果中显示另一个名为“Non-2xx responses”的统计项，用于统计这部分请求数，这些请求并不算在失败的请求中。
Total transferred 表示所有请求的响应数据长度总和，包括每个HTTP响应数据的头信息和正文数据的长度。注意这里不包括HTTP请求数据的长度，仅仅为web服务器流向用户PC的应用层数据总长度。
HTML transferred表示所有请求的响应数据中正文数据的总和，也就是减去了Total transferred中HTTP响应数据中的头信息的长度。

*Requests per second 吞吐率
*Time per request 用户平均请求等待时间
*Time per requet(across all concurrent request)服务器平均请求等待时间，

Transfer rate表示这些请求在单位时间内从服务器获取的数据长度
Percentage of requests served within a certain time（ms）这部分数据用于描述每个请求处理时间的分布情况，比如测试，80%的请求处理时间都不超过6ms，这个处理时间是指前面的Time per request，即对于单个用户而言，平均每个请求的处理时间。
```



## 四. 聊天室应用

#### HTML5 WebSocket

```
WebSocket 是 HTML5 开始提供的一种在单个 TCP 连接上进行全双工通讯的协议。

WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在 WebSocket API 中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输。

在 WebSocket API 中，浏览器和服务器只需要做一个握手的动作，然后，浏览器和服务器之间就形成了一条快速通道。两者之间就直接可以数据互相传送。

```

##### tornado使用websocket

```python
class ChatHandler(tornado.websocket.WebSocketHandler):
    user_list = []
    def open(self, *args: str, **kwargs: str):
        self.user_list.append(self)
        for user in self.user_list:
            username = self.get_secure_cookie('username').decode()
            user.write_message('%s enter room' % username)
            
    def on_message(self, message):
        for user in self.user_list:
            username = self.get_secure_cookie('username').decode()
            user.write_message('%s:%s' % (username,message))

    def on_close(self):
        self.user_list.remove(self)
        for user in self.user_list:
            username = self.get_secure_cookie('username').decode()
            user.write_message('%s leave room' % (username))
```

##### html5使用websocket

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">    
    <title>聊天室</title>
    <script src="https://code.jquery.com/jquery-3.0.0.min.js"></script>
</head>
<body>
    <p>当前账号: {{ username }}</p>
    <div id="chat" style="width:300px; height:300px; border:1px solid #000000;">
        <!--聊天窗口-->

    </div>
    <!--输入信息窗口-->
    <input type="text" name="content" id="content">
    <input type="button" id="btn" value="提交">

    <script>
        <!--建立连接-->
        var websocket = new WebSocket('ws://127.0.0.1:80/chat/')
        <!--获取后端返回的数据-->
        websocket.onmessage = function(e){
            console.log(e.data)
            $('#chat').append('<br>')
            $('#chat').append(e.data)
        }
        $('#btn').click(function(){
            <!--向后端发送数据-->
            var content = $('#content').val()
            websocket.send(content)
        });
    </script>
</body>
  
```


