from flask import Flask, render_template

# __name__作用:指定本文件同级的目录就是根目录
# 默认的静态文件存储位置,就是目录下的static文件夹
# 默认的静态文件访问的地址就是静态路径/static
# 默认提供的模板的存储位置是,根目录下的templates
from app1 import a

app = Flask(__name__, static_url_path='/statics')
class Config:
    DEBUG = True
app.config.from_object(Config)

# 配置文件的加载
# 1.配置文件的加载
@app.route('/')
def hello_world():
    # 返回响应
    # return 'Hello World!'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
