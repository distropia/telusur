# Generated by Django 2.0.4 on 2018-04-26 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20180426_1651'),
        ('polls', '0010_auto_20180426_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='attachment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Attachment'),
        ),
    ]
