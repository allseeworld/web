from django.conf.urls import url

from shopinfto import views

urlpatterns = [
    url(r'infto/',views.Shop_Infto)
]