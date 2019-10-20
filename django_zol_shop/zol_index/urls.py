from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.Shop_List.as_view(), name="show_list"),
]
