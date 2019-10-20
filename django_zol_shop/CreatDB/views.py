import os

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

# from Zol.settings import BASE_DIR
from CreatDB.models import ShopList, ShopInfo
from myfunction.Shop_Analyze import creat, files_jd


class Paage(APIView):
    def get(self, request):
        files = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(files + '\\templates\\index.html')
        creat(files + '\\templates\\index.html')
        return Response('ok')


class Files_jd(APIView):
    def get(self, request):
        files_jd()
        return Response('ok')


class Files_deal(APIView):
    def get(self, request):
        get_queryset = ShopList.objects.all()
        for s, i in enumerate(get_queryset):
            print(s, i)
            i.image_url = i.image_url.split("'")[-2]
            i.save()
            print(i.image_url)

        return Response('ok')


