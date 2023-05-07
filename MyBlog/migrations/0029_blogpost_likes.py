# Generated by Django 4.1.8 on 2023-04-16 22:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MyBlog', '0028_replycomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(related_name='blogpost_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
