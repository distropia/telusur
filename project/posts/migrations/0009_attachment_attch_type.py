# Generated by Django 2.0.4 on 2018-04-26 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='attch_type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]