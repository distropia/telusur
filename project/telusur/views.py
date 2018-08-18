from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

def index(request):
    return render(request, 'pages/home/home-index.html')