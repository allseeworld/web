from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from CreatDB.models import ShopList
from CreatDB.models_serializer import Res_ShopList


class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100


# class Resquest(object):
#     pass


class Shop_List(ListAPIView):
    serializer_class = Res_ShopList
    pagination_class = StandardPageNumberPagination
    queryset = ShopList.objects.all()

    def get(self, request, *args, **kwargs):
        if kwargs['small_id'] != "0":
            self.queryset = self.queryset.filter(small_id=kwargs['small_id']).all()
        elif kwargs['big_id']:
            self.queryset = self.queryset.filter(big_id=kwargs['big_id']).all()
        else:
            pass
        return self.list(request, *args, **kwargs)

    #
    def list(self, request , *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        list_lun = []
        print(serializer.data)

        for ser in serializer.data:
            i = dict(ser)

            # print(dict(i))
            dic = {
                      "id": i['id'],
                      "img": i['image_url'],
                      "goodimg": {
                          "big": i['image_url'],
                          "small": [
                              {"img": i['image_url']},
                              # {"img": i['image_url']},
                              # {"img": i['image_url']},
                          ]
                      },
                      "a": i['introduction'][:4],
                      "p": i['introduction'],
                      "price": i['price']
                  },

            list_lun.append(*dic)
        return Response(list_lun)
