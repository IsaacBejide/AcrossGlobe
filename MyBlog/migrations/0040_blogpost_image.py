# Generated by Django 4.1.8 on 2023-04-18 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyBlog', '0039_remove_blogpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/%Y/%m/%d/'),
        ),
    ]
