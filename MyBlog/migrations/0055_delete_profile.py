# Generated by Django 4.1.8 on 2023-04-30 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyBlog', '0054_alter_blogpost_content'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
