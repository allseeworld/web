from django.contrib import admin


# Register your models here.
from zol_index.models import Shop_Show


class Show_ShopAdmin(admin.ModelAdmin):
    list_display = ['show_name', 'type_id1', 'type_id2', 'type_id3', 'shop_id1', 'shop_id2', 'shop_id3',
                    'shop_id4', 'shop_id5', 'shop_id6', 'shop_id7', 'shop_id8', 'shop_id9']
    list_filter = ['type_id1', 'type_id2', 'type_id3']


admin.site.register(Shop_Show, Show_ShopAdmin)
