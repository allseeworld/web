from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from CreatDB.models import ShopInfo
from CreatDB.models_serializer import Res_ShopInfo


class Shop_Infto2(APIView):
    def get(self, request, shop_id):
        shop = ShopInfo.objects.filter(id=shop_id).first()
        shop = Res_ShopInfo(shop).data
        shop['kind'] =eval(shop['kind'])
        return Response(shop, 200)


class Shop_Infto(View):
    def get(self, request, shop_id):
        shop = ShopInfo.objects.filter(id=shop_id).first()
        shop = Res_ShopInfo(shop).data
        shop['kind'] =eval(shop['kind'])
        return render(request, 'goodsdetail.html', shop)
