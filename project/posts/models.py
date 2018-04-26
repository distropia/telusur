from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Attachment(models.Model):
    title = models.CharField(max_length=200, null=True)
    url = models.TextField(null=True)
    attch_type = models.CharField(max_length=200, null=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField(null=True)
    url = models.TextField(null=True)
    attachment = models.ForeignKey(Attachment, null=True, on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)