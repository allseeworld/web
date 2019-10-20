from rest_framework.response import Response
from rest_framework.views import APIView
from CreatDB.models import TypeShop, TypeShop2, ShopList
from CreatDB.models_serializer import Res_TypeShop, Res_TypeShop2
from zol_index.models import Shop_Show


def show():
    shop = Shop_Show.objects.all()
    dict_shop = {}
    for i in shop:
        a = 0
        # 分隔数据信息
        shop_ids = list(dict(i.__dict__).items())[6:]
        shop_list_ids = list(dict(i.__dict__).items())[3:6]
        id_list = []
        for s in shop_list_ids:
            shop_list_id = s[1]
            if shop_list_id:
                id_list.append(shop_list_id)
        shops = ShopList.objects.filter(big_id__in=id_list).all()
        lists = []
        for shop_id in shop_ids:
            g = 0
            if shop_id[1] != 0:
                g = 1
                shop = ShopList.objects.filter(id=shop_id[1]).first()
            elif len(shops):
                g = 1
                # 防止重复取同一个类的商品
                a += 1
                shop = shops[a]

            if g:
                # 防止没有id的商品加入报错
                lists += [shop.id, shop.image_url]
        dict_shop[i.show_name] = lists
    return dict_shop


class Shop_List(APIView):

    def get(self, request):
        big_leis = []
        for b in range(1,10):

            OTypeShop = TypeShop.objects.filter(group=b).order_by('id')
            res_TypeShop = Res_TypeShop(OTypeShop, many=True).data
            data_shop = []
            for i in res_TypeShop:
                OTypeShop2 = TypeShop2.objects.filter(Fisrt_id=i['id']).order_by('id')
                res_TypeShop2 = Res_TypeShop2(OTypeShop2, many=True).data
                data_shop.append([i, res_TypeShop2])
                # print(res_TypeShop2)
            big_leis.append(data_shop)

        shop_show = show()

        shop_show['lei'] = big_leis

        return Response(shop_show, template_name='ss.html')
