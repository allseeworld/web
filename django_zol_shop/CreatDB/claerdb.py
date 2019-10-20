from django.conf import settings

from CreatDB.models import ShopList, ShopInfo



def clers():
    shop_list = ShopList.objects.all()
    for shoplist in shop_list:
        re = ShopInfo().objects.filter(shop_list_id=shoplist.id)
        if not re :
            print(shop_list.id)
            continue
        else:
            print(re)
            print(shop_list.intersection)


