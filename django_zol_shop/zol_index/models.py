from django.db import models


# Create your models here.

class Shop_Show(models.Model):
    show_name = models.CharField(max_length=64, verbose_name='展示区的名字', default='')
    type_id1 = models.IntegerField(verbose_name='商品大类id1', default=0)
    type_id2 = models.IntegerField(verbose_name='商品大类id2', default=0)
    type_id3 = models.IntegerField(verbose_name='商品大类id3', default=0)
    shop_id1 = models.IntegerField(verbose_name='商品id1', default=0)
    shop_id2 = models.IntegerField(verbose_name='商品id2', default=0)
    shop_id3 = models.IntegerField(verbose_name='商品id3', default=0)
    shop_id4 = models.IntegerField(verbose_name='商品id4', default=0)
    shop_id5 = models.IntegerField(verbose_name='商品id5', default=0)
    shop_id6 = models.IntegerField(verbose_name='商品id6', default=0)
    shop_id7 = models.IntegerField(verbose_name='商品id7', default=0)
    shop_id8 = models.IntegerField(verbose_name='商品id8', default=0)
    shop_id9 = models.IntegerField(verbose_name='商品id9', default=0)

    class Meta:
        verbose_name = '商品展示列表'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
