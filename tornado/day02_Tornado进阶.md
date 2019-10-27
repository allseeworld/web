## Day02 Tornado 进阶

### 一. 请求处理器RequestHandler

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

##### 练习： 登录功能

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


## 二，项目拆分：

#### 1，目录结构

```bash
├── app
│   ├── __init__.py		
│   ├── urls.py                 #url放的地方
│   └── views.py				#类视图放的地方
├── manager.py					#运行app
├── static						#静态文件
└── templates					#模板
    ├── index.html
    └── login.html
    
```

#### 2,文件

##### 	urls.py

```python
from tornado.web import url
from app.views import *

urlpatterns = [
        url(r'/index/', IndexHandler, name='index'),
        url(r'/login/', LoginHandler, name='login'),
        url(r'/logout/', LogoutHandler, name='logout'),
    ]
```

##### 	views.py

```python
import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_cookie('username')
        print(username,type('username'))
        self.render('index.html', username=username)
```

##### 	 _ _init__.py

```python
import tornado.web
from app.urls import urlpatterns
import os
from tornado.options import options

def make_app():
    return tornado.web.Application(handlers=urlpatterns,
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_path= os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
    debug=options.debug,
 )

```

##### 	manage.py

```python
import tornado.ioloop
from app import make_app
from tornado.options import define, options, parse_command_line

define('port', default=8080)
define('debug', default=True)

parse_command_line()
app = make_app()
app.listen(options.port)

tornado.ioloop.IOLoop.current().start()
```



## 三，模板语法

##### 模板: 

​	静态html + 模板语言

##### 注释：

​	 {# 注解内容 #}

##### 变量： 

​	{{ 变量名 }}

​	{{ age  }}

##### 标签:  

​	 {%  %}

##### if 标签:

​	{%  if  条件%}  

​	{% end %}

​			

​	{% if 条件 %} 

​	{% elif 条件%} 

​	{% else %} 

​	 {% end %}

##### for标签:

​	{% for i in [1, 2, 3, 4] %} 

​		<p>{{ i }}</p>

​	{% end %}

##### block

```
  {% block title %}
  {% end %}
    
继承
   {% extends 'base.html' %}

   {% block css %}
        <!--第一种加载方式: 直接定义静态文件的路径-->
        <!--<link rel="stylesheet" href="/static/css/style.css">-->
        <!--第二种加载方式-->
        <link rel="stylesheet" href="{{ static_url('css/style.css') }}">
   {% end %}
```

