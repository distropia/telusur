# Generated by Django 2.0.4 on 2018-04-26 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_attachment_attch_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='attachment',
        ),
    ]