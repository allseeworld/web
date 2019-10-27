# 接收命令行参数,并启动项目
from tornado import ioloop
from tornado.options import parse_command_line, options

from App import make_app

parse_command_line()
app = make_app()
app.listen(options.port)
ioloop.IOLoop.current().start()
