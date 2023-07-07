# Generated by Django 4.1.6 on 2023-07-06 11:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupchat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(-1), related_name='owned_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]