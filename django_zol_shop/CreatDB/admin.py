from django.contrib import admin

# Register your models here.
from CreatDB.models import ShopList, ShopInfo, TypeShop2, TypeShop


class TypeShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']


class TypeShop2Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'Fisrt_id']
    list_filter = ['Fisrt_id']
    search_fields = ['id', 'name']


class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'introduction', 'price', 'inventory', 'kind', 'sales', 'Image', 'image_url',
                    'shop_list_id']
    list_filter = ['name']
    search_fields = ['id', 'name', 'price']


class ShopListAdmin(admin.ModelAdmin):

    # def image_url(self):
    #     print(self.image_url())
    #     return self.image_url.
        # return self.image_url.

    list_display = ['id', 'introduction', 'price', 'Image', 'image_url', 'big_id', 'small_id']
    list_filter = ['big_id', 'small_id']
    search_fields = ['id', 'name', 'price']
    # image_url.admin_order_field = 'image_url'


verbose_name = '创建数据'
admin.site.register(TypeShop, TypeShopAdmin)
admin.site.register(TypeShop2, TypeShop2Admin)
admin.site.register(ShopInfo, ShopInfoAdmin)
admin.site.register(ShopList, ShopListAdmin)
