from django.conf.urls import url

from shopinfto import views

urlpatterns = [

    url(r'^infto/(?P<shop_id>[0-9]+)/',views.Shop_Infto.as_view()),
    url(r'^infto2/(?P<shop_id>[0-9]+)/',views.Shop_Infto2.as_view())
]