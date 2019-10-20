from rest_framework import serializers

from CreatDB.models import TypeShop, TypeShop2


class Res_TypeShop(serializers.ModelSerializer):

    class Meta:
        model = TypeShop
        fields = '__all__'

    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.name


class Res_TypeShop2(serializers.ModelSerializer):
    class Meta:
        model = TypeShop2
        fields = '__all__'
    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.name


class Res_ShopInfo(serializers.Serializer):
    name = serializers.CharField(max_length=64, label='名字')
    introduction = serializers.CharField(max_length=256, label='商品简介')
    price = serializers.FloatField(label='价格')
    inventory = serializers.IntegerField(label='库存')
    kind = serializers.CharField(label='种类')
    sales = serializers.IntegerField(label='销量')
    Image = serializers.ImageField(label='图片')
    image_url = serializers.URLField(label='图片地址')
    shop_list_id = serializers.CharField(max_length=256, label='列表商品id')

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.name


class Res_ShopList(serializers.Serializer):
    id = serializers.IntegerField(label="id")
    # name = serializers.CharField(max_length=64,label='名字')
    introduction = serializers.CharField(max_length=256, label='商品简介')
    price = serializers.FloatField(label='价格')
    # inventory = serializers.IntegerField(label='库存')
    # kind = serializers.TextField(label='种类')
    # sales = serializers.IntegerField(label='销量')
    Image = serializers.ImageField(label='图片')
    image_url = serializers.URLField(label='图片地址')
    big_id = serializers.CharField(max_length=256, label='大类id')
    small_id = serializers.CharField(max_length=256, label='小类id')
