import string

from .models import Post
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def create_random_posts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        Post.objects.create("username=username", email=email, password=password)
    return '{} random posts created with success!'.format(total)