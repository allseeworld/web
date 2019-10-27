## Day01 Tornado基础

### Tornado概述 

Python的Web框架种类繁多（比Python语言的关键字还要多），但在众多优秀的Web框架中，Tornado框架最适合用来开发需要处理长连接和应对高并发的Web应用。Tornado框架在设计之初就考虑到性能问题，它可以处理大量的并发连接，更轻松的应对C10K（万级并发）问题，是非常理想的实时通信Web框架。

Tornado框架源于FriendFeed网站，在FriendFeed网站被Facebook收购之后得以开源，正式发布的日期是2009年9月10日。Tornado能让你能够快速开发高速的Web应用，如果你想编写一个可扩展的社交应用、实时分析引擎，或RESTful API，那么Tornado框架就是很好的选择。Tornado其实不仅仅是一个Web开发的框架，它还是一个高性能的事件驱动网络访问引擎，内置了高性能的HTTP服务器和客户端（支持同步和异步请求），同时还对WebSocket提供了完美的支持。 

了解和学习Tornado最好的资料就是它的官方文档，在[tornadoweb.org](http://www.tornadoweb.org)上面有很多不错的例子，你也可以在Github上找到Tornado的源代码和历史版本。



### 5分钟上手Tornado

1. 创建并激活虚拟环境。

   ```Shell
   mkvirtualenv tornadoenv
   ```

2. 安装Tornado。

   ```Shell
   pip install tornado
   ```

3. 编写Web应用。

   ```Python
   import tornado.ioloop
   import tornado.web

   class MainHandler(tornado.web.RequestHandler):
      def get(self):
          self.write('<h1>Hello, world!</h1>')
           
   def main():
      app = tornado.web.Application(handlers=[(r'/', MainHandler), ])
      app.listen(8888)
      tornado.ioloop.IOLoop.current().start()

   if name == 'main':
       main()
   ```



4. 运行并访问应用。

   ```Shell
   python example01.py
   ```



### 使用命令行参数动态设置端口

```Python
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line

# 定义默认端口
define('port', default=8000, type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<h1>Hello, world!</h1>')

def main():
    # python example01.py --port=8888
    parse_command_line()
    app = tornado.web.Application(handlers=[(r'/', MainHandler), ])
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
```

在启动Web应用时，如果没有指定端口，将使用`define`函数中设置的默认端口8000，如果要指定端口，可以使用下面的方式来启动Web应用。

```Shell
python example01.py --port=8888
```



### 路由解析

上面我们曾经提到过创建`Application`实例时需要指定`handlers`参数，这个参数非常重要，它应该是一个元组的列表，元组中的第一个元素是正则表达式，它用于匹配用户请求的资源路径；第二个元素是`RequestHandler`的子类。在刚才的例子中，我们只在`handlers`列表中放置了一个元组，事实上我们可以放置多个元组来匹配不同的请求（资源路径），而且可以使用正则表达式的捕获组来获取匹配的内容并将其作为参数传入到`get`、`post`这些方法中。

```Python
import os
import random

import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line

# 定义默认端口
define('port', default=8000, type=int)

class DaysHandler(tornado.web.RequestHandler):
    # def get(self, year, month, day):
    def get(self, month, day, year):
        self.write('%s年%s月%s日' % (year, month, day))

class Days2Handler(tornado.web.RequestHandler):
    # def get(self, year, month, day):
    def get(self, month, year, day):
        self.write('%s年%s月%s日' % (year, month, day))
        
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

def main():
    """主函数"""
    parse_command_line()
    app = tornado.web.Application(
        # handlers是按列表中的顺序依次进行匹配的
        handlers=[
        	(r'/days/(\d{4})/(\d+)/(\d{2})/', DaysHandler),
        	(r'/days2/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/', Days2Handler),
        ],
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates'),
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
```

模板页index.html。

```HTML
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Tornado基础</title>
</head>
<body>
	<h1>{{message}}</h1>
</body>
</html>
```



### 请求处理器RequestHandler

RequestHandler是处理用户请求的核心类，通过重写`get`、`post`、`put`、`delete`等方法可以处理不同类型的HTTP请求，除了这些方法之外，`RequestHandler`还实现了很多重要的方法，下面是部分方法的列表：

1. `get_argument` / `get_arguments` / `get_body_argument` / `get_body_arguments` / `get_query_arugment` / `get_query_arguments`：获取请求参数。

2. `set_status` / `send_error` ：操作状态码和响应头。

3. `write` / `flush` / `finish` /：和输出相关的方法。

4. `render` / `render_string`：渲染模板。

5. `redirect`：请求重定向。

6. `get_cookie` / `set_cookie` /  `clear_cookie` / `clear_all_cookies`：操作Cookie。

7. `reverse_url` : url反向解析

   redirect(reverse_url(''))

   ​

   #### 登录功能

```Python
# 登录验证，并设置cookie
class UserHander(tornado.web.RequestHandler):
    def get(self):
        username = self.get_query_argument('username')
        password = self.get_query_argument('password')

        if username == 'hule' and password == '123456':
            self.set_cookie('username',username,expires_days=7)

            self.redirect('/index/')
        else:
            self.write('登录失败')

```

##### login.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="{{ reverse_url('u_handler') }}">
        用户名：<input type="text" name="username">
        password：<input type="text" name="password">
        <input type="submit" value="登录">
    </form>
</body>
</html>
```

##### index.html

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!--<link rel="stylesheet" href="/static/index.css">-->
    <link rel="stylesheet" href="{{ static_url('index.css')}}">
</head>
<body>
    <h3>index</h3>
    <p>{{ message }}</p>
    {% if username %}
        <p>{{username}}</p>
    {% end %}
    <a href="{{ reverse_url('login') }}">登录</a>
</body>
</html>

```

