# Generated by Django 4.1.8 on 2023-05-10 07:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MyBlog', '0059_delete_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='viewers',
            field=models.ManyToManyField(blank=True, editable=False, null=True, related_name='viewed_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
