from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, JsonResponse
from posts.models import Post, Category
import logging
import json

logger = logging.getLogger(__name__)

def index(request):
    latest_posts = Post.objects.all().order_by('-pub_date')[:10]
    most_viewed_posts = Post.objects.all().order_by('-views')[:10]
    categories = Category.objects.all().exclude(id=1)[:5]

    context = {
        'latest_posts': latest_posts,
        'most_viewed_posts': most_viewed_posts,
        'categories': categories
    }

    return render(request, 'pages/home/home-index.html', context)