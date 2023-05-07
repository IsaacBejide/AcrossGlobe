# Generated by Django 4.1.8 on 2023-04-24 09:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MyBlog', '0050_alter_blogpost_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='posts_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
