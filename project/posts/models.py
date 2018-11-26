import os

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from datetime import datetime


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, max_length=200)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, max_length=200)
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Attachment(models.Model):
    title = models.CharField(max_length=200, null=True)
    path = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to='static/attachments', default='static/attachments/00.jpg')
    attch_type = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "<a href=\"%s\">%s</a>" % (os.path.join(os.path.abspath(self.path)), self.title)

    __str__.allow_tags = True


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=True, editable=False, related_name="author", on_delete=models.SET_NULL)
    editor = models.ForeignKey(User, null=True, editable=False, related_name="editor", on_delete=models.SET_NULL)
    content = RichTextField(null=True)
    url = models.TextField(null=True, editable=False)
    slug = models.SlugField(unique=True, null=True, max_length=200, editable=False)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag) 
    attachment = models.ImageField(null=True)
    publish = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    views = models.IntegerField(null=True, default=0, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.pk is None:
            now = datetime.now()
            self.url = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + "/" + slugify(self.title)
            self.slug = slugify(self.title)
        super(Post, self).save(force_insert, force_update, *args, **kwargs)
