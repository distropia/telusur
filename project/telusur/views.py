from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, JsonResponse
from posts.models import Post, Category
import logging
from .utils import *
from django.core import serializers


logger = logging.getLogger(__name__)


def index(request):
    latest_posts = Post.objects.all().order_by('-pub_date')[:15]
    most_viewed_posts = Post.objects.all().order_by('-views')[:10]
    categories = Category.objects.all().exclude(id=1)[:5]

    category_id = request.GET.get('cat', '')
    if category_id is not None and category_id != '':
        posts_by_categories = Post.objects.\
                                  filter(categories__in=[category_id]). \
                                  exclude(attachment__isnull=True). \
                                  order_by('-pub_date')[:8]
        logger.debug(dump(posts_by_categories))
    else:
        category_id = 0
        posts_by_categories = latest_posts[:8]

    context = {
        'latest_posts': latest_posts,
        'most_viewed_posts': most_viewed_posts,
        'categories': categories,
        'posts_by_categories': posts_by_categories,
        'category_id': category_id,
        'posts': latest_posts
    }

    print('category_id', category_id)

    return render(request, 'pages/home/home-index.html', context)


def post_detail(request, slug):
    categories = Category.objects.all().exclude(id=1)[:5]
    latest_posts = Post.objects.\
                       exclude(attachment__isnull=True).\
                       order_by('-pub_date')[:10]
    most_viewed_posts = Post.objects.all().order_by('-views')[:10]
    post = Post.objects.get(slug=slug)

    context = {
        'post': post,
        'categories': categories,
        'latest_posts': latest_posts,
        'most_viewed_posts': most_viewed_posts,
    }

    return render(request, 'pages/post-detail/post-detail-index.html', context)


def post_by_category(request, category_id):
    latest_posts = Post.objects.all().order_by('-pub_date')[:10]
    most_viewed_posts = Post.objects.all().order_by('-views')[:10]
    categories = Category.objects.all().exclude(id=1)[:5]
    posts = Post.objects.\
                filter(categories__in=[category_id]). \
                exclude(attachment__isnull=True). \
                order_by('-pub_date')[:8]

    context = {
        'latest_posts': latest_posts,
        'most_viewed_posts': most_viewed_posts,
        'categories': categories,
        'posts': posts
    }

    return render(request, 'pages/post-category/post-category-index.html', context)


def test(request):
    return render(request, 'default.html')
