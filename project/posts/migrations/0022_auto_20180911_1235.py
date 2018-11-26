# Generated by Django 2.0.4 on 2018-09-11 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_post_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='attachment',
            name='image',
            field=models.ImageField(default='static/attachments/00.jpg', null=True, upload_to='static/attachments'),
        ),
    ]