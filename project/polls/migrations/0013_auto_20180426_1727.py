# Generated by Django 2.0.4 on 2018-04-26 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20180426_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
