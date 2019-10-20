from django.conf.urls import url

from CreatDB import views

urlpatterns = [
    url(r'pa/', views.Paage.as_view(), name='pa'),
    url(r'jd/', views.Files_jd.as_view(), name='jd'),
    url(r'deal/', views.Files_deal.as_view(), name='deal'),
]
