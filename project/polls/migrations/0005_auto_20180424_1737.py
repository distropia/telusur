# Generated by Django 2.0.4 on 2018-04-24 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20180424_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='url',
            field=models.TextField(null=True),
        ),
    ]
