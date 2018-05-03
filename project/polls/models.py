import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from posts.models import Attachment, Tag
from ckeditor.fields import RichTextField


class Question(models.Model):
    title = models.CharField(max_length=200, null=True)
    question_text = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = RichTextField(null=True)
    url = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    attachment = models.ForeignKey(Attachment, null=True, on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    attachment = models.ForeignKey(Attachment, null=True, on_delete=models.CASCADE)
    votes = models.IntegerField(null=True, default=0)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.choice_text


class Information(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=200)
    useragent = models.TextField(null=True)
    created_at = models.DateTimeField()