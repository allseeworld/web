from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


def Shop_Infto(request):

    book = 'sdasdad'

    return render(request, 'index.html', {'books': book})
