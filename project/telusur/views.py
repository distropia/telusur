from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, JsonResponse
from posts.models import Post
import logging
import json

logger = logging.getLogger(__name__)

def index(request):
    posts = Post.objects.all().order_by('-pub_date')[:10]

    context = {
        'posts': posts
    }

    return render(request, 'pages/home/home-index.html', context)