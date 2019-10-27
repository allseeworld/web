# Day03 Tornado模型

## 一. 模型基础

#### ORM介绍

```python
ORM(Object Relational Mapping)对象关系映射，是一种程序技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。

Tornado默认并没有提供任何数据库操作的API
我们可以选择任何适合自己项目的数据库来使用
Tornado中可以自己的选择用原生SQL语句实现功能，也可以选择ORM（SQLAlchemy）

原生SQL缺点:
  代码利用率低，条件复杂代码语句越长，有很多相似语句
  一些SQL是在业务逻辑中拼出来的，修改需要了解业务逻辑
  直接写SQL容易忽视SQL问题
    
使用ORM:
   Tornado通过Model操作数据库，不管你数据库的类型是MySql或者Sqlite，Tornado会帮你生成相应数据库类型的SQL语句，所以不需要关注SQL语句和类型，对数据的操作Tornado帮我们自动完成。只要会写Model就可以了。
	ORM：将对对象的操作转换为原生SQL.
	ORM优点：
        易用性，可以有效减少重复SQL
        性能损耗少
        设计灵活，可以轻松实现复杂查询
        移植性好

ORM原理:
    模型类结构   =>  数据库表结构
     属性       =>    表的字段
     对象       =>  表的一条数据          
```



## 二. Tornado使用ORM

#### ORM： sqlalchemy

```
tornado, 没有集成orm对象，我们可以调用第三方的库: sqlalchemy
```

#### 安装

```
pip install sqlalchemy
pip install pymysql
```

#### 使用：

##### 初始化sqlalchemy：

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 连接数据库格式
# mysql配置
db_url = 'mysql+pymysql://root:123456@127.0.0.1:3306/tornadodb'

# 创建引擎，建立连接
engine = create_engine(db_url)

# 模型与数据库表进行关联的基类，模型必须继承于Base
Base = declarative_base(bind=engine)

# 创建session会话：用于模型操作
DbSession = sessionmaker(bind=engine)
session = DbSession()

```

##### 创建模型类

```python
from sqlalchemy import Column, Integer, String
from utils.conn import Base

# 映射模型对应的表
def create_db():
	Base.metadata.create_all()

# 删除模型映射的表
def drop_db():
    Base.metadata.drop_all()

class Student(Base):
      __tablename__ = 'student'
      # 主键自增的int类型的id主键
      id = Column(Integer, primary_key=True, autoincrement=True)
      # 定义不能为空的唯一的姓名字段
      s_name = Column(String(10), unique=True, nullable=False)
      s_age = Column(Integer, default=18)

```


#### 单表操作

##### 增

```python
# 创建单条数据
stu = Student()
stu.s_name = 'xiaoming'
session.add(stu)
session.commit()

# 创建多条数据
stus = []
for i in range(10):
    stu = Student()
    stu.s_name = 'xiaoming_%s' % i
    stus.append(stu)

session.add_all(stus)
session.commit()

```

##### 删

```python
# 用filter改
session.query(User).filter_by(age=2).delete()
session.query(User).filter(User.id==1).delete()
session.commit()
	
# 对象删
user = session.query(User).get(4)
session.delete(user)
session.commit()
```

##### 改

```python
# 用filter改
session.query(User).filter(User.id<4, User.id>=2).update({'age':2})   #传字典
session.commit()

# 用对象改
user = session.query(User).get(3)
user.name = ‘changjia'
session.commit()
```

##### 查

```python
#根据id查询，获取一个类的对象
session.query(User).get(2)

#批量查询
#查询所有记录
session.query(User).all()

# filter_by
# filter
session.query(User).filter_by(name='lala').all()

# first() 取到第一个
# count() 总数

# filter
session.query(User).filter(User.name=='lala').all()
session.query(User).filter(User.id >=1).all()
session.query(User).filter(User.id < 10).all()
session.query(User).filter(User.id <=1).all()

session.query(User).filter(User.name.startswith('la')).all()  #  like "la%"
session.query(User).filter(User.name.endswith('la')).all()  # like "%la"
session.query(User).filter(User.name.contains('y')).all()  # like "%y%"

session.query(User).filter(User.id<4, User.id>=2).all()  # and

```



#### 多表操作（扩展）

##### 一对多

```python
# 模型创建：用户和收货地址
#  User:Address = 1:N
#   ps: 1个用户有多个收货地址，1个收货地址只属于1个用户

# 用户模型
class User(Base):
    __tablename__ = 'user'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    age = Column(Integer, default=18)
    sex = Column(Boolean, default=True)
    created = Column(DateTime, default='2019-8-27')
    # 关系
    addresss = relationship('Address', backref='user')

    def __str__(self):
        return self.name + "-" + str(self.age)

# 收货地址模型
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    # 外键
    userid = Column(Integer, ForeignKey(User.id))


    
# 一对多模型操作
class AddressHandler(tornado.web.RequestHandler):
    def get(self):
        # 某用户的所有地址
        user = session.query(User).get(2)
        print(user.addresss)

        # 某地址所属的用户
        addr = session.query(Address).get(1)
        print(addr.user)
        print(addr.userid, addr.user.id, addr.user.name)

        self.write('ok')

```

##### 多对多（了解）

```python
# 多对多模型创建
collect = Table(
    'collect',
    Base.metadata,
    Column('userid', Integer, ForeignKey('user2.id'), primary_key=True),
    Column('movieid', Integer, ForeignKey('movie.id'), primary_key=True)
)

class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)

class User2(Base):
    __tablename__ = 'user2'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    # 关联
    movies = relationship('Movie', backref='users', secondary=collect)

```



##### 作业： 创建User模型，实现登录注册功能

​	使用post请求， 需要传参

