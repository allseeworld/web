# views.py:存放类视图
#   存放RequestHandler
from abc import ABC

from tornado import web
from .models import *


# 类视图
class IndexHandler(web.RequestHandler, ABC):
    def get(self):
        name = "wansicong"
        age = 31
        likes = ["雪梨", "逗得", "杨幂", "哈士奇", ]
        user = {
            "身高": 170,
            "体重": 150
        }
        date = {
            "name": name,
            "age": age,
            "likes":likes,
            "user": user
        }
        # self.render("index.html",**date)
        self.render("child.html")
