# Generated by Django 2.0.4 on 2018-04-27 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20180426_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posttag',
            name='post',
        ),
        migrations.RemoveField(
            model_name='posttag',
            name='tag',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='posts.Tag'),
        ),
        migrations.DeleteModel(
            name='PostTag',
        ),
    ]
