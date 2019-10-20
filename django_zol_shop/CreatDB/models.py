from django.db import models


# Create your models here.

class TypeShop(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='大类')
    group = models.IntegerField( verbose_name='组',default=0)

    class Meta:
        verbose_name = '商品大类'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.name


class TypeShop2(models.Model):
    name = models.CharField(max_length=64, verbose_name='小类')
    Fisrt_id = models.CharField(max_length=5, verbose_name='大类id')

    class Meta:
        verbose_name = '商品小类'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.name


class ShopInfo(models.Model):
    name = models.CharField(max_length=64, verbose_name='名字')
    introduction = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.FloatField(verbose_name='价格')
    inventory = models.IntegerField(verbose_name='库存')
    kind = models.TextField(verbose_name='种类')
    sales = models.IntegerField(verbose_name='销量')
    Image = models.ImageField(verbose_name='图片')
    image_url = models.URLField(verbose_name='图片地址')
    shop_list_id = models.CharField(max_length=256, verbose_name='列表商品id')

    class Meta:
        verbose_name = '商品详细信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.name


class ShopList(models.Model):
    # name = models.CharField(max_length=64,verbose_name='名字')
    introduction = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.FloatField(verbose_name='价格')
    # inventory = models.IntegerField(verbose_name='库存')
    # kind = models.TextField(verbose_name='种类')
    # sales = models.IntegerField(verbose_name='销量')
    Image = models.ImageField(verbose_name='图片')
    image_url = models.URLField(verbose_name='图片地址')
    big_id = models.CharField(max_length=256, verbose_name='大类id')
    small_id = models.CharField(max_length=256, verbose_name='小类id')


    class Meta:
        verbose_name = '商品列表信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
