from django.conf.urls import url

from sholist import views

urlpatterns = [
    url(r'^list/(?P<big_id>[0-9]+)/(?P<small_id>[0-9]+)/', views.Shop_List.as_view())
]
